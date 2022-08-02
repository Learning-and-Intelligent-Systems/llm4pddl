"""Utility functions."""

import os
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import List, Optional

from pyperplan.planner import HEURISTICS, SEARCHES, search_plan


def validate_plan(domain_file: str, problem_file: str,
                  plan: List[str]) -> bool:
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
    val_binary = val_dir / platform_dir / "Validate"
    cmd_str = f"{val_binary} -v {domain_file} {problem_file} {plan_file}"
    output = subprocess.getoutput(cmd_str)
    os.remove(plan_file)
    if "Plan valid" in output:
        return True
    return False


def run_planning(domain_file: str, problem_file: str, heuristic: str = "hff", search: str = "gbf") -> Optional[List[str]]:
    """Find a plan with pyperplan."""
    search_fn = SEARCHES[search]
    heuristic_fn = HEURISTICS[heuristic]
    pyperplan_plan = search_plan(
        domain_file,
        problem_file,
        search_fn,
        heuristic_fn,
    )
    if pyperplan_plan is None:
        return None
    return [a.name for a in pyperplan_plan]
