"""Data structures."""
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class Task:
    """A task is a PDDL domain file and problem file."""
    domain_file: Path
    problem_file: Path
