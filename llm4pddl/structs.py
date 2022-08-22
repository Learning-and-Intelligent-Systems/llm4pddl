"""Data structures."""
from dataclasses import dataclass
from functools import cached_property
from pathlib import Path
from typing import Any, Dict, List

from pyperplan.pddl.pddl import Action as _PyperplanAction
from pyperplan.pddl.pddl import Domain as _PyperplanDomain
from pyperplan.pddl.pddl import Predicate as _PyperplanPredicate
from pyperplan.pddl.pddl import Problem as _PyperplanProblem
from pyperplan.pddl.pddl import Type as _PyperplanType

# Explicitly list the pyperplan data structures that we use.
PyperplanAction = _PyperplanAction
PyperplanDomain = _PyperplanDomain
PyperplanObject = str
PyperplanPredicate = _PyperplanPredicate
PyperplanProblem = _PyperplanProblem
PyperplanType = _PyperplanType


@dataclass(frozen=True)
class Task:
    """A task is a PDDL domain file and problem file."""
    domain_file: Path
    problem_file: Path

    @cached_property
    def task_id(self) -> str:
        """A unique identifier for this task."""
        # Use the name of the domain from the domain file.
        with open(self.domain_file, "r", encoding="utf-8") as f:
            domain_str = f.read()
        domain_tag = "(domain "
        assert domain_str.count(domain_tag) == 1
        domain_tag_idx = domain_str.index(domain_tag)
        tag_close_rel_idx = domain_str[domain_tag_idx:].index(")")
        start = domain_tag_idx + len(domain_tag)
        end = domain_tag_idx + tag_close_rel_idx
        domain_name = domain_str[start:end].strip()
        assert domain_name
        # Use the problem filename, which is assumed unique within the domain.
        assert self.problem_file.name.endswith(".pddl")
        problem_name = self.problem_file.name[:-len(".pddl")]
        return f"{domain_name}__{problem_name}"

    @cached_property
    def task_size(self) -> int:
        """Length of the problem string."""
        with open(self.problem_file, "r", encoding="utf-8") as f:
            problem_str = f.read()
        return len(problem_str)


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
