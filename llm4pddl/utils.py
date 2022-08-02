"""Utility functions."""

import os
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any, Dict, Optional

from pyperplan.planner import HEURISTICS, SEARCHES, search_plan

from llm4pddl.flags import FLAGS
from llm4pddl.structs import Plan, Task


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
    cmd_str = f"{val} -v {task.domain_file} {task.problem_file} {plan_file}"
    output = subprocess.getoutput(cmd_str)
    os.remove(plan_file)
    if "Plan valid" in output:
        return True
    return False


def run_planning(task: Task,
                 heuristic: str = "hff",
                 search: str = "gbf") -> Optional[Plan]:
    """Find a plan with pyperplan."""
    search_fn = SEARCHES[search]
    heuristic_fn = HEURISTICS[heuristic]
    pyperplan_plan = search_plan(
        task.domain_file,
        task.problem_file,
        search_fn,
        heuristic_fn,
    )
    if pyperplan_plan is None:
        return None
    return [a.name for a in pyperplan_plan]


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


def reset_flags(args: Dict[str, Any]) -> None:
    """Resets FLAGS for use in unit tests."""
    FLAGS.__dict__.clear()
    FLAGS.__dict__.update(args)
