"""Tests for PurePlanningApproach()."""

from llm4pddl import utils
from llm4pddl.approaches.pure_planning_approach import PurePlanningApproach
from llm4pddl.envs import create_env


def test_pure_planning_approach():
    """Tests for PurePlanningApproach()."""
    utils.reset_flags({"num_train_tasks": 0, "num_eval_tasks": 3})
    approach = PurePlanningApproach()
    env = create_env("pyperplan-blocks")
    for task in env.get_eval_tasks():
        plan = approach.solve(task)
        assert plan is not None
        assert utils.is_valid_plan(task, plan)
