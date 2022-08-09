"""Environments module."""

from llm4pddl.envs.base_env import BaseEnv
from llm4pddl.envs.pyperplan_env import PyperplanEnv
from llm4pddl.envs.custom_env import CustomEnv


def create_env(env_name: str) -> BaseEnv:
    """Create an environment."""
    if env_name.startswith("pyperplan-"):
        _, benchmark_name = env_name.split("-", 1)
        return PyperplanEnv(benchmark_name)
    elif env_name.startswith("custom-"):
        _, benchmark_name = env_name.split("-", 1)
        return CustomEnv(benchmark_name)
    raise NotImplementedError(f"Unrecognized env name: {env_name}")
