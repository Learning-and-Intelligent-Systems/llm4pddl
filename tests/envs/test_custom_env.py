"""Tests custom_env.py."""

from llm4pddl import utils
from llm4pddl.envs import CUSTOM_BENCHMARKS
from llm4pddl.envs.custom_env import CustomEnv


def test_custom_env():
    """Tests for CustomEnv()"""
    utils.reset_flags({"num_train_tasks": 5, "num_eval_tasks": 10})
    for env_name in CUSTOM_BENCHMARKS:
        env = CustomEnv(env_name)
        assert env.get_name() == f'custom-{env_name}'
        training_tasks = env.get_train_tasks()
        assert len(training_tasks) == 5
        eval_tasks = env.get_eval_tasks()
        assert len(eval_tasks) == 10
        for task_num, train_task in enumerate(training_tasks):
            task_num += 1
            assert train_task.domain_file == utils.get_custom_task(
                env_name, task_num).domain_file