"""Base approach class."""

import abc

from llm4pddl.src.structs import Dataset, Domain, Solution, Task


class BaseApproach(abc.ABC):
    """Base approach class."""

    def __init__(self, domain: Domain) -> None:
        self._domain = domain

    @abc.abstractmethod
    def get_name(self) -> str:
        """Returns the approach name."""
        raise NotImplementedError("Override me!")

    @property
    @abc.abstractmethod
    def is_learning_based(self) -> bool:
        """Returns whether the approach should be trained."""
        raise NotImplementedError("Override me!")

    @abc.abstractmethod
    def learn_from_demonstrations(self, demos: Dataset) -> None:
        """Learn anything from a dataset of demonstrations."""
        raise NotImplementedError("Override me!")

    @abc.abstractmethod
    def solve(self, task: Task) -> Solution:
        """Find a solution to a task, possibly raising an ApproachFailure."""
        raise NotImplementedError("Override me!")
