"""Data structures."""
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List


@dataclass(frozen=True)
class Task:
    """A task is a PDDL domain file and problem file."""
    domain_file: Path
    problem_file: Path


# A plan is currently just a list of strings, where each string is one ground
# operator, e.g., (unstack a b). We may change this later.
Plan = List[str]

# Metrics are saved during evaluation.
TaskMetrics = Dict[str, Any]
# Maps a task string identifier to task metrics.
Metrics = Dict[str, TaskMetrics]
