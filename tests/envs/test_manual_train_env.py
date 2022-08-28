"""Tests for ManualTrainEnv()."""

from llm4pddl import utils
from llm4pddl.envs import MANUAL_TRAIN_BENCHMARKS
from llm4pddl.envs.manual_train_env import ManualTrainEnv


def test_manual_train_env():
    """Tests for ManualTrainEnv()."""
    utils.reset_flags({
        "num_train_tasks": 1,
        "num_eval_tasks": 10,
        "train_task_offset": 0
    })
    for env_name in MANUAL_TRAIN_BENCHMARKS:
        env = ManualTrainEnv(env_name)
        assert env.get_name() == f'manual-{env_name}'
        training_tasks = env.get_train_tasks()
        assert len(training_tasks) == 1
        eval_tasks = env.get_eval_tasks()
        assert len(eval_tasks) == 10
