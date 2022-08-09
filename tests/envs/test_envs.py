"""Tests for the envs module."""

import pytest

from llm4pddl import utils
from llm4pddl.envs import create_env


def test_create_env():
    """Tests for create_env()."""
    # Test pyperplan env.
    utils.reset_flags({"num_train_tasks": 3, "num_eval_tasks": 6})
    blocks_env = create_env("pyperplan-blocks")
    assert blocks_env.get_name() == "pyperplan-blocks"
    train_tasks = blocks_env.get_train_tasks()
    assert len(train_tasks) == 3
    eval_tasks = blocks_env.get_eval_tasks()
    assert len(eval_tasks) == 6
    # Test custom env.
    dressed_env = create_env("custom-dressed")
    assert dressed_env.get_name() == "custom-dressed"
    train_tasks = dressed_env.get_train_tasks()
    assert len(train_tasks) == 3
    eval_tasks = dressed_env.get_eval_tasks()
    assert len(eval_tasks) == 6
    # Test unrecognized env.
    with pytest.raises(NotImplementedError) as e:
        create_env("not a real environment")
    assert "Unrecognized env" in str(e)
