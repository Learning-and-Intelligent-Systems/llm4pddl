"""Tests for PurePlanningApproach()."""

from llm4pddl import utils
from llm4pddl.approaches.pure_planning_approach import PurePlanningApproach
from llm4pddl.envs import create_env


def test_pure_planning_approach():
    """Tests for PurePlanningApproach()."""
    utils.reset_flags({
        "num_train_tasks": 0,
        "num_eval_tasks": 2,
        "python_plan_max_nodes_created": 10000
    })
    approach = PurePlanningApproach()
    assert not approach.is_learning_based
    assert approach.is_planning_based
    env = create_env("pyperplan-blocks")
    for task in env.get_eval_tasks():
        plan, metrics = approach.solve(task)
        assert plan is not None
        assert utils.validate_plan(task, plan)
        assert metrics["nodes_created"] > metrics["nodes_expanded"]
