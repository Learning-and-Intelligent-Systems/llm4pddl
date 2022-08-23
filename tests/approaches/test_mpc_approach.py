"""Tests for MPCApproach()."""

from llm4pddl import utils
from llm4pddl.approaches.mpc_approach import MPCApproach
from llm4pddl.approaches.pure_planning_approach import PurePlanningApproach
from llm4pddl.envs import create_env


def test_mpc_approach():
    """Tests for MPCApproach()."""
    utils.reset_flags({
        "num_train_tasks": 0,
        "num_eval_tasks": 2,
        "planner": "pyperplan",
        "planning_timeout": 100,
        "mpc_max_steps": 100,
    })
    wrapped_approach = PurePlanningApproach()
    approach = MPCApproach(wrapped_approach)
    assert not approach.is_learning_based
    assert approach.is_planning_based
    env = create_env("pyperplan-blocks")
    for task in env.get_eval_tasks():
        plan, metrics = approach.solve(task)
        assert plan is not None
        assert utils.validate_plan(task, plan)
        assert metrics["nodes_created"] > metrics["nodes_expanded"]
