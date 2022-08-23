"""Tests for AugmentedEnv()."""

from llm4pddl import utils
from llm4pddl.envs import AUGMENTED_BENCHMARKS
from llm4pddl.envs.augmented_env import AugmentedEnv


def test_augmented_env():
    """Tests for AugmentedEnv()."""
    utils.reset_flags({"num_train_tasks": 5, "num_eval_tasks": 10})
    for env_name in AUGMENTED_BENCHMARKS:
        env = AugmentedEnv(env_name)
        assert env.get_name() == f'augmented-{env_name}'
        training_tasks = env.get_train_tasks()
        assert len(training_tasks) == 5
        eval_tasks = env.get_eval_tasks()
        assert len(eval_tasks) == 10
