"""Utility functions."""

import functools
import logging
import os
import re
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any, Dict, Optional, Tuple

import numpy as np
from pyperplan.pddl.parser import Parser
from pyperplan.planner import HEURISTICS, SEARCHES, search_plan

from llm4pddl.flags import FLAGS
from llm4pddl.structs import Plan, PyperplanDomain, PyperplanPredicate, \
    PyperplanProblem, PyperplanType, Task, TaskMetrics


def validate_plan(task: Task, plan: Plan) -> bool:
    """Use VAL to check if a plan solves a PDDL problem."""
    plan_str = ""
    for t, action in enumerate(plan):
        plan_str += f"{t}: {action}\n"
    plan_file = tempfile.NamedTemporaryFile(delete=False).name
    with open(plan_file, "w", encoding="utf-8") as f:
        f.write(plan_str)
    val_dir = Path(__file__).parent / "third_party" / "val"
    if sys.platform == "darwin":  # pragma: no cover
        platform_dir = "darwin"
    else:
        assert sys.platform.startswith("linux")
        platform_dir = "linux64"
    val = val_dir / platform_dir / "Validate"
    cmd_str = (f'"{val}" -v "{task.domain_file}" "{task.problem_file}" '
               f'"{plan_file}"')
    output = subprocess.getoutput(cmd_str)
    os.remove(plan_file)
    if "Plan valid" in output:
        return True
    return False


def run_planning(
        task: Task,
        rng: np.random.Generator,
        planner: str = "pyperplan") -> Tuple[Optional[Plan], TaskMetrics]:
    """Find a plan."""
    if planner == "pyperplan":
        return run_pyperplan_planning(task, rng)
    if planner == "fastdownward":  # pragma: no cover
        return run_fastdownward_planning(task)
    if planner == "fastdownward-hff-gbfs":  # pragma: no cover
        return run_fastdownward_planning(task,
                                         alias=None,
                                         search="eager_greedy([ff()])")
    raise NotImplementedError(f"Unrecognized planner: {planner}")


def run_pyperplan_planning(
        task: Task,
        rng: np.random.Generator,
        heuristic: str = "hff",
        search: str = "gbf") -> Tuple[Optional[Plan], TaskMetrics]:
    """Find a plan with pyperplan."""
    search_fn = SEARCHES[search]
    heuristic_fn = HEURISTICS[heuristic]
    # Quiet the pyperplan logging.
    logging.disable(logging.ERROR)
    pyperplan_plan, metrics = search_plan(
        task.domain_file,
        task.problem_file,
        search_fn,
        heuristic_fn,
        rng=rng,
        timeout=FLAGS.planning_timeout,
    )
    logging.disable(logging.NOTSET)
    if pyperplan_plan is None:
        return None, metrics
    return [a.name for a in pyperplan_plan], metrics


def run_fastdownward_planning(
    task: Task,
    alias: Optional[str] = "lama-first",
    search: Optional[str] = None,
) -> Tuple[Optional[Plan], TaskMetrics]:  # pragma: no cover
    """Find a plan with fast downward.

    Usage: Build and compile the Fast Downward planner, then set the environment
    variable FD_EXEC_PATH to point to the `downward` directory. For example:
    1) git clone https://github.com/ronuchit/downward.git
    2) cd downward && ./build.py
    3) export FD_EXEC_PATH="<your absolute path here>/downward"
    """
    # Specify either a search flag or an alias.
    assert (search is None) + (alias is None) == 1
    # The SAS file isn't actually used, but it's important that we give it a
    # name, because otherwise Fast Downward uses a fixed default name, which
    # will cause issues if you run multiple processes simultaneously.
    sas_file = tempfile.NamedTemporaryFile(delete=False).name
    # Run Fast Downward followed by cleanup. Capture the output.
    assert "FD_EXEC_PATH" in os.environ, \
        "Please follow the instructions in the docstring of this method!"
    if alias is not None:
        alias_flag = f"--alias {alias}"
    else:
        alias_flag = ""
    if search is not None:
        search_flag = f"--search '{search}'"
    else:
        search_flag = ""
    fd_exec_path = os.environ["FD_EXEC_PATH"]
    exec_str = os.path.join(fd_exec_path, "fast-downward.py")
    int_timeout = int(np.ceil(FLAGS.planning_timeout))
    cmd_str = (f'"{exec_str}" {alias_flag} '
               f'--search-time-limit {int_timeout} '
               f'--sas-file {sas_file} '
               f'"{task.domain_file}" "{task.problem_file}" '
               f'{search_flag}')
    output = subprocess.getoutput(cmd_str)
    cleanup_cmd_str = f"{exec_str} --cleanup"
    subprocess.getoutput(cleanup_cmd_str)
    # Parse and log metrics.
    if "Time limit has been reached" in output:
        num_nodes_expanded = re.findall(r"(\d+) expanded", output)[-1]
        num_nodes_created = re.findall(r"(\d+) evaluated", output)[-1]
    else:
        num_nodes_expanded = re.findall(r"Expanded (\d+) state", output)[0]
        num_nodes_created = re.findall(r"Evaluated (\d+) state", output)[0]
    metrics = {
        "nodes_expanded": float(num_nodes_expanded),
        "nodes_created": float(num_nodes_created)
    }
    # Extract the plan from the output, if one exists.
    if "Solution found!" not in output:
        return None, metrics
    if "Plan length: 0 step" in output:
        # Handle the special case where the plan is found to be trivial.
        return [], metrics
    plan_str = re.findall(r"(.+) \(\d+?\)", output)
    assert plan_str  # already handled empty plan case, so something went wrong
    plan = [f"({a})" for a in plan_str]
    return plan, metrics


def get_pyperplan_benchmark_task(benchmark_name: str, task_num: int) -> Task:
    """Get the paths to the pyperplan benchmark domain and problem files."""
    pyperplan_dir = Path(__file__).parent / "third_party" / "pyperplan"
    domain_dir = pyperplan_dir / "benchmarks" / benchmark_name
    standard_domain_file = domain_dir / "domain.pddl"
    if os.path.exists(standard_domain_file):
        domain_file = standard_domain_file
    else:
        domain_file_name = f"domain{task_num:02d}.pddl"
        domain_file = domain_dir / domain_file_name
    if not os.path.exists(domain_file):
        raise FileNotFoundError(f"Domain not found: {domain_file}")
    problem_file_name = f"task{task_num:02d}.pddl"
    problem_file = domain_dir / problem_file_name
    if not os.path.exists(problem_file):
        raise FileNotFoundError(f"Problem not found: {problem_file}")
    return Task(domain_file, problem_file)


def get_custom_task(benchmark_name: str, task_num: int) -> Task:
    """Get the paths to the custom domain and problem files."""
    domain_dir = Path(
        __file__).parent / "envs" / "assets" / "pddl" / benchmark_name
    domain_file = domain_dir / "domain.pddl"
    if not os.path.exists(domain_file):
        raise FileNotFoundError(f"Domain not found: {domain_file}")
    problem_file = domain_dir / f"task{str(task_num).zfill(2)}.pddl"
    if not os.path.exists(problem_file):
        raise FileNotFoundError(f"Task not found: {problem_file}")
    return Task(domain_file, problem_file)


@functools.lru_cache(maxsize=None)
def parse_task(task: Task) -> Tuple[PyperplanDomain, PyperplanProblem]:
    """Parse a task into Pyperplan structs."""
    parser = Parser(task.domain_file, task.problem_file)
    domain = parser.parse_domain()
    problem = parser.parse_problem(domain)
    return (domain, problem)


def pred_to_str(pred: PyperplanPredicate) -> str:
    """Create a string representation of a Pyperplan predicate (atom)."""
    arg_str = " ".join(str(o) for o, _ in pred.signature)
    return f"{pred.name}({arg_str})"


def is_subtype(type1: PyperplanType, type2: PyperplanType) -> bool:
    """Checks whether type1 inherits from type2."""
    while type1 is not None:
        if type1 == type2:
            return True
        type1 = type1.parent
    return False


def reset_flags(args: Dict[str, Any], default_seed: int = 123) -> None:
    """Resets FLAGS for use in unit tests.

    Unless seed is specified, we use a default for testing.
    """
    FLAGS.__dict__.clear()
    FLAGS.__dict__.update(args)
    if "seed" not in FLAGS:
        FLAGS.__dict__["seed"] = default_seed


@functools.lru_cache(maxsize=None)
def get_git_commit_hash() -> str:
    """Return the hash of the current git commit."""
    out = subprocess.check_output(["git", "rev-parse", "HEAD"])
    return out.decode("ascii").strip()


def get_config_path_str() -> str:
    """Get a string identifier for an experiment from FLAGS."""
    return f"{FLAGS.env}__{FLAGS.approach}__{FLAGS.seed}__{FLAGS.experiment_id}"
