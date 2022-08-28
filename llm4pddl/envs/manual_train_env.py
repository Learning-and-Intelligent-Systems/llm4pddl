"""Environments with manually engineered train tasks."""

from pathlib import Path

from llm4pddl import utils
from llm4pddl.envs.multi_dir_env import MultiDirEnv


class ManualTrainEnv(MultiDirEnv):
    """An environment with manually engineered train tasks."""

    @property
    def env_prefix(self) -> str:
        return "manual"

    @property
    def dir_path(self) -> Path:
        return utils.MANUAL_TRAIN_BENCHMARK_DIR
