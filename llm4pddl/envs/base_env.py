"""Base class for environments."""

import abc
from typing import List

from llm4pddl.structs import Task


class BaseEnv(abc.ABC):
    """Base class for an environment."""

    @abc.abstractmethod
    def get_name(self) -> str:
        """Get the name of the environment."""
        raise NotImplementedError("Override me!")

    @abc.abstractmethod
    def get_train_tasks(self) -> List[Task]:
        """Get train tasks."""
        raise NotImplementedError("Override me!")

    @abc.abstractmethod
    def get_eval_tasks(self) -> List[Task]:
        """Get test tasks."""
        raise NotImplementedError("Override me!")
