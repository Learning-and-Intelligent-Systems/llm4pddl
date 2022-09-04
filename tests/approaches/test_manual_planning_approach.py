"""Tests for ManualPlanningApproach()."""

import pytest

from llm4pddl import utils
from llm4pddl.approaches.manual_planning_approach import ManualPlanningApproach
from llm4pddl.envs import create_env


@pytest.mark.parametrize("env_name", [
    "pyperplan-blocks", "pyperplan-gripper", "pyperplan-miconic",
    "pyperplan-logistics", "pyperplan-satellite"
])
def test_manual_planning_approach(env_name):
    """Tests for ManualPlanningApproach()."""
    utils.reset_flags({
        "num_train_tasks": 2,
        "num_eval_tasks": 1,
        "train_task_offset": 0,
        "planner": "pyperplan",
        "planning_timeout": 100
    })
    approach = ManualPlanningApproach()
    assert not approach.is_learning_based
    assert not approach.is_planning_based
    env = create_env(env_name)
    for task in env.get_eval_tasks():
        plan, _ = approach.solve(task)
        assert plan is not None
        assert utils.validate_plan(task, plan)
