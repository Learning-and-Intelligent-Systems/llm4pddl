"""Pyperplan benchmark environments."""

from typing import List

from llm4pddl import utils
from llm4pddl.envs.base_env import BaseEnv
from llm4pddl.flags import FLAGS
from llm4pddl.structs import Task


class PyperplanEnv(BaseEnv):
    """An environment defined by a pyperplan benchmark."""

    def __init__(self, benchmark_name: str) -> None:
        self._benchmark_name = benchmark_name
        # Load tasks from pyperplan and sort them by size (just problem string
        # length). Then pick the shortest ones for the training set.
        all_tasks = []
        i = 1
        # Keep loading until a file is not found.
        while True:
            try:
                task = utils.get_pyperplan_benchmark_task(benchmark_name, i)
            except FileNotFoundError:
                # Reached the end of the tasks.
                break
            all_tasks.append(task)
            i += 1
        # We need to have at least this number of tasks.
        assert len(all_tasks) >= FLAGS.num_train_tasks + FLAGS.num_eval_tasks

        # Sort from smallest to largest.
        sorted_tasks = sorted(all_tasks, key=utils.get_task_size)
        # Split into train and eval.
        self._train_tasks = sorted_tasks[:FLAGS.num_train_tasks]
        self._eval_tasks = sorted_tasks[FLAGS.num_train_tasks:(
            FLAGS.num_train_tasks + FLAGS.num_eval_tasks)]

    def get_name(self) -> str:
        return f"pyperplan-{self._benchmark_name}"

    def get_train_tasks(self) -> List[Task]:
        return list(self._train_tasks)

    def get_eval_tasks(self) -> List[Task]:
        return list(self._eval_tasks)
