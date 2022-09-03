"""Tests for dataset.py."""

import shutil

import pytest

from llm4pddl import utils
from llm4pddl.dataset import create_dataset
from llm4pddl.envs import create_env

MANUAL_ENVS = ["pyperplan-blocks", "pyperplan-gripper"]


@pytest.mark.parametrize("env_name", MANUAL_ENVS)
def test_manual_data_generation(env_name):
    """Tests for manual data generation."""
    data_dir = "_fake_data_dir"
    num_train_tasks = 2
    utils.reset_flags({
        "env": env_name,
        "num_train_tasks": num_train_tasks,
        "num_eval_tasks": 1,
        "train_task_offset": 0,
        "data_dir": data_dir,
        "data_gen_method": "manual",
        "load_data": False,
    })
    env = create_env(env_name)
    train_tasks = env.get_train_tasks()
    dataset = create_dataset(train_tasks)
    assert len(dataset) == num_train_tasks
    for d in dataset:
        assert utils.validate_plan(d.task, d.solution)
    shutil.rmtree(data_dir)
