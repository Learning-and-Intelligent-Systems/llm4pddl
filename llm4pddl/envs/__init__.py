"""Environments module."""

from llm4pddl.envs.augmented_env import AugmentedEnv
from llm4pddl.envs.base_env import BaseEnv
from llm4pddl.envs.custom_env import CustomEnv
from llm4pddl.envs.manual_train_env import ManualTrainEnv
from llm4pddl.envs.pyperplan_env import PyperplanEnv


def create_env(env_name: str) -> BaseEnv:
    """Create an environment."""
    if env_name.startswith("pyperplan-"):
        _, benchmark_name = env_name.split("-", 1)
        return PyperplanEnv(benchmark_name)
    if env_name.startswith("custom-"):
        _, benchmark_name = env_name.split("-", 1)
        return CustomEnv(benchmark_name)
    if env_name.startswith("augmented-"):
        _, benchmark_name = env_name.split("-", 1)
        return AugmentedEnv(benchmark_name)
    if env_name.startswith("manual-"):
        _, benchmark_name = env_name.split("-", 1)
        return ManualTrainEnv(benchmark_name)
    raise NotImplementedError(f"Unrecognized env name: {env_name}")
