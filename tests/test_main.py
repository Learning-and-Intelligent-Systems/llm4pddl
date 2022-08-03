"""Tests for main.py."""

import shutil
import sys
import tempfile

from llm4pddl import utils
from llm4pddl.approaches.base_approach import BaseApproach
from llm4pddl.envs import create_env
from llm4pddl.main import _main, _run_evaluation, _run_pipeline


def test_main():
    """Tests for main.py."""
    # Create a temporary results dir so as to not pollute real results.
    temp_results_dir = tempfile.TemporaryDirectory().name
    # Test successful pipeline run with pure planning in blocks.
    sys.argv = [
        "dummy", "--env", "pyperplan-blocks", "--approach", "pure-planning",
        "--num_train_tasks", "0", "--num_eval_tasks", "2", "--results_dir",
        temp_results_dir
    ]
    _main()  # should run
    # Remove temporary results dir.
    shutil.rmtree(temp_results_dir)


class _MockApproach(BaseApproach):

    def __init__(self, plan_sequence):
        self.remaining_plans = plan_sequence

    @property
    def is_learning_based(self) -> bool:
        return True

    def get_name(self):
        return "dummy"

    def solve(self, task):
        return self.remaining_plans.pop(0)


def test_run_pipeline():
    """Tests for _run_pipeline() in main.py."""
    # Create a temporary results dir so as to not pollute real results.
    temp_results_dir = tempfile.TemporaryDirectory().name
    utils.reset_flags({
        "env": "pyperplan-blocks",
        "approach": "dummy",
        "num_train_tasks": 0,
        "num_eval_tasks": 2,
        "results_dir": temp_results_dir
    })
    # Cover cases where approach is None or invalid.
    plan_sequence = [None, []]
    approach = _MockApproach(plan_sequence)
    assert approach.get_name() == "dummy"
    env = create_env("pyperplan-blocks")
    _run_pipeline(approach, env)
    # Remove temporary results dir.
    shutil.rmtree(temp_results_dir)


def test_run_evaluation():
    """Tests for _run_evaluation() in main.py."""
    utils.reset_flags({"num_train_tasks": 0, "num_eval_tasks": 2})
    # Cover cases where approach is None or invalid.
    plan_sequence = [None, []]
    approach = _MockApproach(plan_sequence)
    assert approach.get_name() == "dummy"
    env = create_env("pyperplan-blocks")
    eval_tasks = env.get_eval_tasks()
    results = _run_evaluation(approach, eval_tasks)
    assert set(results) == set(eval_tasks)
    task0, task1 = eval_tasks
    assert results[task0]["result"] == "no_plan_found"
    assert results[task1]["result"] == "invalid_plan"
