"""Pyperplan benchmark environments."""

from pathlib import Path

from llm4pddl import utils
from llm4pddl.envs.single_dir_env import SingleDirEnv


class PyperplanEnv(SingleDirEnv):
    """An environment defined by a pyperplan benchmark."""

    @property
    def env_prefix(self) -> str:
        return "pyperplan"

    @property
    def dir_path(self) -> Path:
        return utils.PYPERPLAN_BENCHMARK_DIR
