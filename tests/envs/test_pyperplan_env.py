"""Tests for PyperplanEnv()."""

from llm4pddl import utils
from llm4pddl.envs.pyperplan_env import PyperplanEnv


def test_pyperplan_env():
    """Tests for PyperplanEnv()."""
    utils.reset_flags({"num_train_tasks": 5, "num_eval_tasks": 10})
    benchmark_names = [
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
    for benchmark_name in benchmark_names:
        env = PyperplanEnv(benchmark_name)
        assert env.get_name() == f"pyperplan-{benchmark_name}"
        train_tasks = env.get_train_tasks()
        assert len(train_tasks) == 5
        eval_tasks = env.get_eval_tasks()
        assert len(eval_tasks) == 10
