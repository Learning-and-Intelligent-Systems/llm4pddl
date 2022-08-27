"""Custom environments."""

from pathlib import Path

from llm4pddl import utils
from llm4pddl.envs.single_dir_env import SingleDirEnv


class CustomEnv(SingleDirEnv):
    """A custom made environment."""

    @property
    def env_prefix(self) -> str:
        return "custom"

    @property
    def dir_path(self) -> Path:
        return utils.CUSTOM_BENCHMARK_DIR
