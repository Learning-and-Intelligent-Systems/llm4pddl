"""Utility functions."""

import functools
import hashlib
import logging
import os
import re
import subprocess
import sys
import tempfile
from collections import defaultdict
from pathlib import Path
from typing import Any, Collection, Dict, Optional, Sequence, Set, Tuple

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from pyperplan.grounding import ground as pyperplan_ground
from pyperplan.pddl.parser import Parser
from pyperplan.planner import HEURISTICS, SEARCHES, search_plan

from llm4pddl.flags import FLAGS
from llm4pddl.structs import Plan, PyperplanAction, PyperplanDomain, \
    PyperplanPredicate, PyperplanProblem, PyperplanType, Task, TaskMetrics

LLM_QUESTION_TOKEN = "Q:"
LLM_ANSWER_TOKEN = "A:"


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


@functools.lru_cache(maxsize=None)
def get_all_ground_operators(task: Task) -> Dict[str, PyperplanAction]:
    """Ground all operators in a task.

    Returns a dict mapping the string name of the operator to the
    operator.
    """
    parser = Parser(task.domain_file, task.problem_file)
    domain = parser.parse_domain()
    problem = parser.parse_problem(domain)
    logging.disable(logging.ERROR)
    pyperplan_task = pyperplan_ground(problem)
    logging.disable(logging.NOTSET)
    return {o.name: o for o in pyperplan_task.operators}


@functools.lru_cache(maxsize=None)
def parse_plan_step(action_str: str, task: Task) -> Optional[PyperplanAction]:
    """Parse a string action into a Pyperplan action (ground operator).

    If the ground operator is invalid, returns None. This can be the
    case when the ground operator has a static precondition that is not
    in the initial state of the task, or if the operator is deemed
    irrelevant for the task based on the relevance analysis in pyperplan
    grounding.
    """
    # Match the action to a ground operator in the set of all ground operators
    # from pyperplan. Note that the grounding is cached for efficiency. We
    # do it this way, rather than reconstructing the operators, because
    # pyperplan grounding removes static preconditions.
    ground_ops = get_all_ground_operators(task)
    return ground_ops.get(action_str, None)


def pred_to_str(pred: PyperplanPredicate) -> str:
    """Create a string representation of a Pyperplan predicate (atom)."""
    arg_str = " ".join(str(o) for o, _ in pred.signature)
    return f"{pred.name}({arg_str})"


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


def get_visualization(input_path: str, output_dir: str) -> None:
    """Creates visualization of planner accuracy across all environments."""
    df = pd.read_csv(input_path)
    column_labels = []
    _ = [column_labels.append(col) for col in df.columns]
    env_column_index = column_labels.index('env')
    approach_column_index = column_labels.index('approach')
    accuracy_column_index = column_labels.index('success')
    experiment_name_index = column_labels.index('experiment_id')

    llm_multi_accuracies = {}
    llm_standard_plan_accuracies = {}
    llm_multi_plan_accuracies = {}
    fd_accuracies = {}
    pyperplan_accuracies = {}
    for _, row_raw in df.iterrows():
        row = row_raw.tolist()
        approach_name = row[approach_column_index]
        environment_name = row[env_column_index]
        accuracy = row[accuracy_column_index]
        accuracy = float(accuracy[0:accuracy.index(' ')])
        experiment_name = row[experiment_name_index]
        if approach_name == "llm-multi":
            llm_multi_accuracies[environment_name] = accuracy
        elif approach_name == "llm-standard-plan":
            llm_standard_plan_accuracies[environment_name] = accuracy
        elif approach_name == "llm-multi-plan":
            llm_multi_plan_accuracies[environment_name] = accuracy
        elif approach_name == "pure-planning" and "fd-only" in experiment_name:
            fd_accuracies[environment_name] = accuracy
        elif approach_name == "pure-planning" and ("pyperplan"
                                                   in experiment_name):
            pyperplan_accuracies[environment_name] = accuracy

    llm_approaches = [
        "standard-plan", "multi", "multi-plan", "fd", "pyperplan"
    ]
    fig, axs = plt.subplots(nrows=5, ncols=6, figsize=(30, 25))
    for ax, env in zip(axs.flat, llm_multi_accuracies.keys()):
        llm_accuracies = [
            llm_standard_plan_accuracies[env], llm_multi_accuracies[env],
            llm_multi_plan_accuracies[env], fd_accuracies[env],
            pyperplan_accuracies[env]
        ]
        ax.bar(llm_approaches, llm_accuracies, color="blue")
        ax.set_title(env)
        ax.set_ylabel("accuracy")
    fig.savefig(output_dir + "/final_output.png",
                facecolor='w',
                bbox_inches="tight",
                pad_inches=0.3,
                transparent=True)
    plt.close(fig)
