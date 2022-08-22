"""Environments created by augmenting tasks."""

from pathlib import Path

from llm4pddl import utils
from llm4pddl.envs.multi_dir_env import MultiDirEnv


class AugmentedEnv(MultiDirEnv):
    """An environment created by augmenting tasks.

    This is different from CustomEnv because we want to make a very clear
    separation between tasks that were augmented from train tasks and held-out
    eval tasks. So we store the tasks in two separate folders per env: train
    and eval.

    This is different from PyperplanEnv because of the augmentation, and
    because we may want to also augment other kinds of tasks.

    Since augmentation takes a while, it should be run once separately from
    the main pipeline; see scripts/run_data_augmentation.py.
    """

    @property
    def env_prefix(self) -> str:
        return "augmented"

    @property
    def dir_path(self) -> Path:
        return utils.AUGMENTED_BENCHMARK_DIR
