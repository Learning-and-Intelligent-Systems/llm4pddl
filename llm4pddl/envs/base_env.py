"""Base class for environments."""

import abc
from typing import List

from llm4pddl import utils
from llm4pddl.flags import FLAGS
from llm4pddl.structs import Task


class BaseEnv(abc.ABC):
    """Base class for an environment."""

    def __init__(self) -> None:
        self._final_train_tasks = None  # set in _create_train_tasks()
        self._final_eval_tasks = None  # set in _create_eval_tasks()

    @abc.abstractmethod
    def get_name(self) -> str:
        """Get the name of the environment."""
        raise NotImplementedError("Override me!")

    def get_train_tasks(self) -> List[Task]:
        """Get the train tasks."""
        if self._final_train_tasks is None:
            self._final_train_tasks = self._create_train_tasks()
            # Augment the original train tasks.
            if FLAGS.augment_train_tasks:
                self._final_train_tasks = utils.augment_tasks(
                    self._final_train_tasks,
                    num_iters=FLAGS.task_augmentation_num_iters)
        return self._final_train_tasks

    def get_eval_tasks(self) -> List[Task]:
        """Get the evaluation tasks."""
        if self._final_eval_tasks is None:
            self._final_eval_tasks = self._create_eval_tasks()
        return self._final_eval_tasks

    @abc.abstractmethod
    def _create_train_tasks(self) -> List[Task]:
        """Create the train tasks (one time only)."""
        raise NotImplementedError("Override me!")

    @abc.abstractmethod
    def _create_eval_tasks(self) -> List[Task]:
        """Create the eval tasks (one time only)."""
        raise NotImplementedError("Override me!")
