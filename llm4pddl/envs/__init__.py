"""Environments module."""

from llm4pddl.envs.augmented_env import AugmentedEnv
from llm4pddl.envs.base_env import BaseEnv
from llm4pddl.envs.custom_env import CustomEnv
from llm4pddl.envs.pyperplan_env import PyperplanEnv

PYPERPLAN_BENCHMARKS = [
    "airport",
    "blocks",
    "depot",
    "elevators",
    "freecell",
    "gripper",
    "logistics",
    "miconic",
    "movie",
    "openstacks",
    "parcprinter",
    "pegsol",
    "psr-small",
    "rovers",
    "satellite",
    "scanalyzer",
    "sokoban",
    "tpp",
    "transport",
    "woodworking",
    "zenotravel",
]

CUSTOM_BENCHMARKS = [
    "dressed", "easy_blocks", "medium_blocks", "easy_delivery",
    "medium_delivery", "easy_spanner", "medium_spanner"
]

ALL_ENVS = [f"pyperplan-{b}" for b in PYPERPLAN_BENCHMARKS
            ] + [f"custom-{b}" for b in CUSTOM_BENCHMARKS]


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
    raise NotImplementedError(f"Unrecognized env name: {env_name}")
