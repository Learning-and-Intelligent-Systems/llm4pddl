"""Tests custom_env.py."""

from llm4pddl import utils
from llm4pddl.envs.custom_env import CustomEnv


def test_custom_env():
    """Tests for CustomEnv()"""
    utils.reset_flags({"num_train_tasks": 5, "num_eval_tasks": 10})
    custom_envs = ['dressed']
    for env in custom_envs:
        Env = CustomEnv(env)
        assert Env.get_name() == f'custom-{env}'
        training_tasks = Env.get_train_tasks()
        assert len(training_tasks) == 5
        eval_tasks = Env.get_eval_tasks()
        assert len(eval_tasks) == 10
        for task_num, train_task in enumerate(training_tasks):
            task_num += 1
            assert train_task.domain_file == utils.get_custom_task(
                env, task_num).domain_file
