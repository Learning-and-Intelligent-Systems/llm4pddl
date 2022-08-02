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
        # Load tasks from pyperplan, and split so that the easiest (lower
        # number) tasks are train, and the harder tasks are eval.
        switch_num = FLAGS.num_train_tasks + 1
        train_task_nums = range(1, switch_num)
        eval_task_nums = range(switch_num, switch_num + FLAGS.num_eval_tasks)
        self._train_tasks = [
            utils.get_pyperplan_benchmark_task(benchmark_name, i)
            for i in train_task_nums
        ]
        self._eval_tasks = [
            utils.get_pyperplan_benchmark_task(benchmark_name, i)
            for i in eval_task_nums
        ]

    def get_name(self) -> str:
        return f"pyperplan-{self._benchmark_name}"

    def get_train_tasks(self) -> List[Task]:
        return list(self._train_tasks)

    def get_eval_tasks(self) -> List[Task]:
        return list(self._eval_tasks)
