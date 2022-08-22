"""Environments created by augmenting tasks."""

from typing import List

from llm4pddl import utils
from llm4pddl.envs.base_env import BaseEnv
from llm4pddl.flags import FLAGS
from llm4pddl.structs import Task


class AugmentedEnv(BaseEnv):
    """An environment created by augmenting tasks.
    
    This is different from CustomEnv because we want to make a very clear
    separation between tasks that were augmented from train tasks and held-out
    eval tasks. So we store the tasks in three separate folders per env: train,
    augmented_train, and eval.

    This is different from PyperplanEnv because of the augmentation, and
    because we may want to also augment other kinds of tasks.

    Since augmentation takes a while, it should be run once separately from
    the main pipeline; see scripts/run_data_augmentation.py.
    """

    def __init__(self, benchmark_name: str) -> None:
        self._benchmark_name = benchmark_name
        # For now, load all train and augmented train tasks and choose the
        # smallest ones to keep. Soon we may replace this by allowing the
        # approach to choose which of the main train tasks it wants to use.


    def get_name(self) -> str:
        return f"augmented-{self._benchmark_name}"

    def get_train_tasks(self) -> List[Task]:
        return list(self._train_tasks)

    def get_eval_tasks(self) -> List[Task]:
        return list(self._eval_tasks)
