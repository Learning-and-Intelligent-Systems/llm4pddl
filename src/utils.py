"""General utility methods."""

import subprocess

from llm4pddl.src.structs import GroundOperator, Solution, Task


class ApproachFailure(Exception):
    """Raised by an approach when it fails to solve a task."""


def get_git_commit_hash() -> str:
    """Return the hash of the current git commit."""
    out = subprocess.check_output(["git", "rev-parse", "HEAD"])
    return out.decode("ascii").strip()


def solution_is_valid(solution: Solution, task: Task) -> bool:
    """Check if a solution solves a task."""
    import ipdb; ipdb.set_trace()
