"""Base class for approaches."""

import abc
from typing import Optional, Sequence

from llm4pddl.structs import Plan, Task


class BaseApproach(abc.ABC):
    """Base class for an approach that solves tasks."""

    @property
    @abc.abstractmethod
    def is_learning_based(self) -> bool:
        """Whether or not this approach should be trained."""
        raise NotImplementedError("Override me!")

    @abc.abstractmethod
    def get_name(self) -> str:
        """Get the approach name."""
        raise NotImplementedError("Override me!")

    @abc.abstractmethod
    def solve(self, task: Task) -> Optional[Plan]:
        """Return a plan, or None if no plan can be found."""
        raise NotImplementedError("Override me!")

    def train(self, train_tasks: Sequence[Task]) -> None:
        """Optionally train the approach from train tasks."""
