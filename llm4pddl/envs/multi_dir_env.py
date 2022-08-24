"""ABC for environments with train/eval tasks in separate directories."""

import abc
from pathlib import Path
from typing import List

from llm4pddl import utils
from llm4pddl.envs.base_env import BaseEnv
from llm4pddl.flags import FLAGS
from llm4pddl.structs import Task


class MultiDirEnv(BaseEnv):
    """ABC for environments with train/eval tasks in separate directories."""

    def __init__(self, benchmark_name: str) -> None:
        self._benchmark_name = benchmark_name
        # Load tasks and sort them by size.
        train_dir = self.dir_path / benchmark_name / "train"
        self._train_tasks = utils.get_all_tasks_from_dir(train_dir)
        start = FLAGS.train_task_offset
        end = start + FLAGS.num_train_tasks
        self._train_tasks = self._train_tasks[start:end]
        assert len(self._train_tasks) == FLAGS.num_train_tasks

        eval_dir = self.dir_path / benchmark_name / "eval"
        self._eval_tasks = utils.get_all_tasks_from_dir(eval_dir)
        assert len(self._eval_tasks) >= FLAGS.num_eval_tasks
        self._eval_tasks = self._eval_tasks[:FLAGS.num_eval_tasks]

    @property
    @abc.abstractmethod
    def env_prefix(self) -> str:
        """Used in constructing the env name."""
        raise NotImplementedError("Override me!")

    @property
    @abc.abstractmethod
    def dir_path(self) -> Path:
        """Path to the directory with the "train" and "eval" subdirs"."""
        raise NotImplementedError("Override me!")

    def get_name(self) -> str:
        return f"{self.env_prefix}-{self._benchmark_name}"

    def get_train_tasks(self) -> List[Task]:
        return list(self._train_tasks)

    def get_eval_tasks(self) -> List[Task]:
        return list(self._eval_tasks)
