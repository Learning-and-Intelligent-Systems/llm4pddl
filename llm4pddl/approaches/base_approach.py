"""Base class for approaches."""

import abc
from typing import Optional

from llm4pddl.structs import Plan, Task


class BaseApproach(abc.ABC):
    """Base class for an approach that solves tasks."""

    @abc.abstractmethod
    def get_name(self) -> str:
        """Get the approach name."""
        raise NotImplementedError("Override me!")

    @abc.abstractmethod
    def solve(self, task: Task) -> Optional[Plan]:
        """Return a plan, or None if no plan can be found."""
        raise NotImplementedError("Override me!")
