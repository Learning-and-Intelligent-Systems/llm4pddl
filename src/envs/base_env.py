"""Base environment class."""

import abc
from typing import List

from llm4pddl.src.structs import Domain, Task


class BaseEnv(abc.ABC):
    """Base environment class."""

    @abc.abstractmethod
    def get_name(self) -> str:
        """Returns the environment name."""
        raise NotImplementedError("Override me!")

    @property
    @abc.abstractmethod
    def domain(self) -> Domain:
        """Returns the environment domain."""
        raise NotImplementedError("Override me!")

    @abc.abstractmethod
    def get_train_tasks(self) -> List[Task]:
        """Returns train tasks."""
        raise NotImplementedError("Override me!")

    @abc.abstractmethod
    def get_test_tasks(self) -> List[Task]:
        """Returns test tasks."""
        raise NotImplementedError("Override me!")
