"""ABC for environments with tasks defined in a single directory."""

import abc
from pathlib import Path
from typing import List

from llm4pddl import utils
from llm4pddl.envs.base_env import BaseEnv
from llm4pddl.flags import FLAGS
from llm4pddl.structs import Task


class SingleDirEnv(BaseEnv):
    """ABC for environments with tasks defined in a single directory."""

    def __init__(self, benchmark_name: str) -> None:
        self._benchmark_name = benchmark_name
        # Load tasks and sort them by size.
        tasks = utils.get_all_tasks_from_dir(self.dir_path / benchmark_name)
        # We need to have at least this number of tasks.
        assert len(tasks) >= FLAGS.num_train_tasks + FLAGS.num_eval_tasks
        # Split into train and eval.
        start = FLAGS.train_task_offset
        switch = start + FLAGS.num_train_tasks
        end = switch + FLAGS.num_eval_tasks
        self._train_tasks = tasks[start:switch]
        self._eval_tasks = tasks[switch:end]
        assert len(self._train_tasks) == FLAGS.num_train_tasks
        assert len(self._eval_tasks) == FLAGS.num_eval_tasks

    @property
    @abc.abstractmethod
    def env_prefix(self) -> str:
        """Used in constructing the env name."""
        raise NotImplementedError("Override me!")

    @property
    @abc.abstractmethod
    def dir_path(self) -> Path:
        """Path to the directory with the tasks."""
        raise NotImplementedError("Override me!")

    def get_name(self) -> str:
        return f"{self.env_prefix}-{self._benchmark_name}"

    def get_train_tasks(self) -> List[Task]:
        return list(self._train_tasks)

    def get_eval_tasks(self) -> List[Task]:
        return list(self._eval_tasks)
