"""Utility functions."""

from typing import List

import tempfile
import os
import subprocess
import sys
from pathlib import Path


def validate_plan(domain_file: str, problem_file: str, plan: List[str]) -> bool:
    """Use VAL to check if a plan solves a PDDL problem."""
    plan_str = ""
    for t, action in enumerate(plan):
        # TODO make sure that string format matches what's expected here
        plan_str += f"{t}: {action}\n"
    plan_file = tempfile.NamedTemporaryFile(delete=False).name
    with open(plan_file, "w") as f:
        f.write(plan_str)
    val_dir = Path(__file__).parent / "third_party" / "val"
    if sys.platform == "darwin":
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
