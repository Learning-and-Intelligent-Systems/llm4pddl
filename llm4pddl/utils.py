"""Utility functions."""

import functools
import hashlib
import logging
import os
import re
import string
import subprocess
import sys
import tempfile
from collections import defaultdict
from pathlib import Path
from typing import Any, Collection, Dict, List, Optional, Sequence, Set, Tuple

import matplotlib.pyplot as plt
import numpy as np
from pyperplan.pddl.parser import Parser
from pyperplan.planner import HEURISTICS, SEARCHES, search_plan

from llm4pddl.flags import FLAGS
from llm4pddl.structs import Plan, PyperplanAction, PyperplanDomain, \
    PyperplanPredicate, PyperplanProblem, PyperplanType, Task, TaskMetrics

# Global constants.
LLM_QUESTION_TOKEN = "Q:"
LLM_ANSWER_TOKEN = "A:"
_DIR = Path(__file__).parent
PYPERPLAN_BENCHMARK_DIR = _DIR / "third_party" / "pyperplan" / "benchmarks"
CUSTOM_BENCHMARK_DIR = _DIR / "envs" / "assets" / "pddl"
AUGMENTED_BENCHMARK_DIR = CUSTOM_BENCHMARK_DIR / "augmented"
MANUAL_TRAIN_BENCHMARK_DIR = CUSTOM_BENCHMARK_DIR / "manual"


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
    logging.debug(output)
    return False


def run_planning(
        task: Task,
        planner: str = "pyperplan") -> Tuple[Optional[Plan], TaskMetrics]:
    """Find a plan."""
    if planner == "pyperplan":
        return run_pyperplan_planning(task)
    if planner == "fastdownward":  # pragma: no cover
        return run_fastdownward_planning(task)
    if planner == "fastdownward-hff-gbfs":  # pragma: no cover
        return run_fastdownward_planning(task,
                                         alias=None,
                                         search="eager_greedy([ff()])")
    raise NotImplementedError(f"Unrecognized planner: {planner}")


def run_pyperplan_planning(
    task: Task,
    heuristic: str = "hff",
    search: str = "gbf",
    partial_plans: Optional[Sequence[Sequence[PyperplanAction]]] = None,
    partial_plan_guidance_method: Optional[str] = None,
) -> Tuple[Optional[Plan], TaskMetrics]:
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
        timeout=FLAGS.planning_timeout,
        partial_plans=partial_plans,
        partial_plan_guidance_method=partial_plan_guidance_method,
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
               f'--overall-time-limit {int_timeout} '
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


def get_task_from_dir(dir_path: Path, task_num: int) -> Task:
    """Get domain and problem file paths from a dir path and task number.

    Problems must be named task01.pddl, task02.pddl, ... etc., or, task1.pddl,
    task2.pddl, ... etc. The former convention is for pyperplan benchmark
    tasks. The latter is for cases where the number of problems may exceed 99.

    For domains, there must either be a single domain file called domain.pddl,
    or one domain file per problem with name domain<task number>.pddl. The
    format of the task number should match that of the problem file.
    """
    if not os.path.exists(dir_path):
        raise FileNotFoundError(f"Domain not found: {dir_path}")
    # Find the task first.
    problem_file_v1 = dir_path / f"task{task_num}.pddl"
    problem_file_v2 = dir_path / f"task{task_num:02d}.pddl"
    if os.path.exists(problem_file_v1):
        problem_file = problem_file_v1
    elif os.path.exists(problem_file_v2):
        problem_file = problem_file_v2
    else:
        raise FileNotFoundError(f"Problem {task_num} not found.")
    # Try the standardized domain file first.
    standard_domain_file = dir_path / "domain.pddl"
    if os.path.exists(standard_domain_file):
        domain_file = standard_domain_file
    # Otherwise, infer the expected name from the problem file.
    else:
        domain_file_name = problem_file.name.replace("task", "domain")
        domain_file = dir_path / domain_file_name
        assert os.path.exists(domain_file)
    return Task(domain_file, problem_file)


def get_all_tasks_from_dir(dir_path: Path) -> List[Task]:
    """Load all tasks from a directory.

    Searches for files named task*.pddl in the given directory.

    Sorts the tasks in order from smallest to largest.
    """
    tasks = []
    for file_path in dir_path.glob("task*.pddl"):
        num = file_path.name[len("task"):-len(".pddl")]
        assert num.isdigit()
        task = get_task_from_dir(dir_path, int(num))
        tasks.append(task)
    # Sort by task size.
    sorted_tasks = sorted(tasks, key=get_task_size)
    return sorted_tasks


def minify_pddl_problem(problem: str) -> str:
    """Maps a string of a problem file to a new string.

    This is for use before querying llm in order to reduce tokens.
    This works by:
    1. Getting rid of space between right parentheses[') )' -> '))'].
    2. Getting rid of space between left parentheses['( (' -> '(('].
    3. Getting rid of leading and trailing whitespace and extra lines after ')'.
    4. Getting rid of '\n' before ')', which are unnecessary.
    This also optionally flattens the problem afterwards by doing:
    5. Getting rid of '\n' between ground atoms, actions, etc.
    6. Getting rid of '\n' between other things and adding a space.
    """
    # Getting rid of space between right parentheses:
    prob_wo_space = ')'.join(
        [piece.strip(' ') for piece in problem.split(')')])
    # Getting rid of space between left parentheses:
    prob_wo_space = '('.join([
        piece.strip(' ') if piece.strip(' ') == '' else piece
        for piece in prob_wo_space.split('(')
    ])
    # Getting rid of leading and trailing whitespace and extra lines after ')':
    prob_wo_whitespace = '\n'.join([
        piece.strip() for piece in prob_wo_space.split('\n')
        if piece.strip() != ''
    ])
    # Getting rid of '\n' before ')', which are unnecessary.
    new_problem = prob_wo_whitespace.replace('\n)', ')')
    if FLAGS.llm_prompt_flatten_pddl:
        # Removing new lines for everything except in init
        partially_flattened = new_problem.replace(')\n(', ')(')
        # Removing new lines in init, a space is needed between
        new_problem = partially_flattened.replace('\n', ' ')
        # Add new lines for the question and answer tokens
        new_problem = new_problem.replace(f'{LLM_ANSWER_TOKEN} ',
                                          f'{LLM_ANSWER_TOKEN}')
        new_problem = new_problem.replace(f' {LLM_ANSWER_TOKEN}',
                                          f'{LLM_ANSWER_TOKEN}')
        new_problem = new_problem.replace(f'{LLM_ANSWER_TOKEN}',
                                          f'\n{LLM_ANSWER_TOKEN}\n')
        new_problem = new_problem.replace(f'{LLM_QUESTION_TOKEN} ',
                                          f'{LLM_QUESTION_TOKEN}')
        new_problem = new_problem.replace(f' {LLM_QUESTION_TOKEN}',
                                          f'{LLM_QUESTION_TOKEN}')
        new_problem = new_problem.replace(f'{LLM_QUESTION_TOKEN}',
                                          f'\n{LLM_QUESTION_TOKEN}\n')
        if new_problem[0] == '\n':
            new_problem = new_problem[1:]
    return new_problem


@functools.lru_cache(maxsize=None)
def parse_task(task: Task) -> Tuple[PyperplanDomain, PyperplanProblem]:
    """Parse a task into Pyperplan structs."""
    parser = Parser(task.domain_file, task.problem_file)
    domain = parser.parse_domain()
    problem = parser.parse_problem(domain)
    return (domain, problem)


def pyperplan_problem_to_str(problem: PyperplanProblem) -> str:
    """Create a PDDL string from a pyperplan problem."""
    # Sort everything to ensure determinism.
    objects_str = "\n    ".join(f"{o} - {problem.objects[o]}"
                                for o in sorted(problem.objects))

    def _atom_to_str(atom: PyperplanPredicate) -> str:
        pred_name = atom.name
        if not atom.signature:
            return f"({pred_name})"
        args_str = " ".join(obj for obj, _ in atom.signature)
        return f"({pred_name} {args_str})"

    init_str = "\n    ".join(_atom_to_str(a) for a in problem.initial_state)
    goal_str = " ".join(_atom_to_str(a) for a in problem.goal)

    return f"""(define (problem {problem.name})
  (:domain {problem.domain.name})
  (:objects\n    {objects_str}
  )
  (:init\n    {init_str}
  )
  (:goal (and {goal_str}))
)
"""


@functools.lru_cache(maxsize=None)
def get_task_size(task: Task) -> int:
    """A crude estimate of problem complexity."""
    _, prob = parse_task(task)
    return len(prob.objects) + len(prob.initial_state) + len(prob.goal)


def pred_to_str(pred: PyperplanPredicate) -> str:
    """Create a string representation of a Pyperplan predicate (atom)."""
    if not pred.signature:
        return f"({pred.name})"
    arg_str = " ".join(str(o) for o, _ in pred.signature)
    return f"({pred.name} {arg_str})"


def group_by_predicate(preds: Collection[PyperplanPredicate]) -> Set[str]:
    """Create a set of strings of the form.

    unary-predicate1: (obj1) (obj2) ...

    or

    binary-predicate2: (obj1, obj2) (obj4, obj3) ...

    etc.
    """
    pred_to_args = defaultdict(set)
    for pred in preds:
        pred_to_args[pred.name].add(tuple(o for o, _ in pred.signature))
    groups = set()
    args_to_str = lambda a: "(" + ",".join(a) + ")"
    for pred in pred_to_args:
        sorted_args = sorted(pred_to_args[pred])
        args_str = " ".join(map(args_to_str, sorted_args))
        group = f"{pred}: {args_str}"
        groups.add(group)
    return groups


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


def str_to_identifier(x: str) -> str:
    """Convert a string to a small string with negligible collision probability
    and where the smaller string can be used to identifier the larger string in
    file names.

    Importantly, this function is deterministic between runs and between
    platforms, unlike python's built-in hash function.

    References:
        https://stackoverflow.com/questions/45015180
        https://stackoverflow.com/questions/5297448
    """
    return hashlib.md5(x.encode('utf-8')).hexdigest()


def randomize_object_names(rng: np.random.Generator,
                           objs: List[str]) -> List[str]:
    """To prevent overfitting, replaces object names in prompt with randomly
    generated strings."""
    random_dict = {}
    for obj in objs:
        if obj not in random_dict:
            random_dict[obj] = ''.join(
                rng.choice(list(string.ascii_lowercase), len(obj)))
    return list(random_dict.values())
