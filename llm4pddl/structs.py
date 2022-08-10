"""Data structures."""
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List

from pyperplan.pddl.pddl import Domain as PyperplanDomain, Problem as PyperplanProblem, Predicate as PyperplanPredicate


@dataclass(frozen=True)
class Task:
    """A task is a PDDL domain file and problem file."""
    domain_file: Path
    problem_file: Path


@dataclass(frozen=True)
class LLMResponse:
    """A single response from a LargeLanguageModel."""
    prompt_text: str
    response_text: str
    tokens: List[str]
    token_logprobs: List[float]
    prompt_info: Dict
    other_info: Dict


# A plan is currently just a list of strings, where each string is one ground
# operator, e.g., (unstack a b). We may change this later.
Plan = List[str]

# Metrics are saved during evaluation.
TaskMetrics = Dict[str, Any]
# Maps a task string identifier to task metrics.
Metrics = Dict[str, TaskMetrics]


@dataclass(frozen=True)
class Datum:
    """A single entry in a training dataset."""
    task: Task
    solution: Plan

# A training dataset.
Dataset = List[Datum]
