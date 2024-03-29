"""Tests for the envs module."""

import pytest

from llm4pddl import utils
from llm4pddl.envs import create_env


@pytest.mark.parametrize("env_name", [
    "pyperplan-blocks", "custom-dressed", "augmented-pyperplan-blocks",
    "manual-pyperplan-gripper"
])
def test_create_env(env_name):
    """Tests for create_env()."""
    utils.reset_flags({
        "num_train_tasks": 1,
        "num_eval_tasks": 6,
        "train_task_offset": 0
    })
    blocks_env = create_env(env_name)
    assert blocks_env.get_name() == env_name
    train_tasks = blocks_env.get_train_tasks()
    assert len(train_tasks) == 1
    eval_tasks = blocks_env.get_eval_tasks()
    assert len(eval_tasks) == 6


def test_create_env_failure():
    """Test failure cases for create_env()."""
    # Test unrecognized env.
    with pytest.raises(NotImplementedError) as e:
        create_env("not a real environment")
    assert "Unrecognized env" in str(e)
