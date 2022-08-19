"""Custom environments."""

from typing import List

from llm4pddl import utils
from llm4pddl.envs.base_env import BaseEnv
from llm4pddl.flags import FLAGS
from llm4pddl.structs import Task


class CustomEnv(BaseEnv):
    """A custom made environment."""

    def __init__(self, benchmark_name: str) -> None:
        super().__init__()
        self._benchmark_name = benchmark_name
        change_num = FLAGS.num_train_tasks + 1
        train_task_nums = range(1, change_num)
        eval_task_nums = range(change_num, change_num + FLAGS.num_eval_tasks)
        self._train_tasks = [
            utils.get_custom_task(benchmark_name, i) for i in train_task_nums
        ]
        self._eval_tasks = [
            utils.get_custom_task(benchmark_name, i) for i in eval_task_nums
        ]

    def get_name(self) -> str:
        return f"custom-{self._benchmark_name}"

    def _create_train_tasks(self) -> List[Task]:
        return list(self._train_tasks)

    def _create_eval_tasks(self) -> List[Task]:
        return list(self._eval_tasks)
