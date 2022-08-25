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
        "--seed", "123", "--num_train_tasks", "0", "--num_eval_tasks", "2",
        "--results_dir", temp_results_dir
    ]
    _main()  # should run
    # Remove temporary results dir.
    shutil.rmtree(temp_results_dir)


class _MockApproach(BaseApproach):

    def __init__(self, plan_sequence):
        super().__init__()
        self.remaining_plans = plan_sequence

    @property
    def is_learning_based(self) -> bool:
        return True

    @property
    def is_planning_based(self) -> bool:
        return False

    def get_name(self):
        return "dummy"

    def solve(self, task):
        return self.remaining_plans.pop(0), {}


def test_run_pipeline():
    """Tests for _run_pipeline() in main.py."""
    # Create a temporary results dir so as to not pollute real results.
    temp_results_dir = tempfile.TemporaryDirectory().name
    # Same for data dir.
    temp_data_dir = tempfile.TemporaryDirectory().name
    utils.reset_flags({
        "env": "pyperplan-blocks",
        "approach": "dummy",
        "experiment_id": "dummy",
        "num_train_tasks": 1,
        "num_eval_tasks": 2,
        "train_task_offset": 0,
        "results_dir": temp_results_dir,
        "data_dir": temp_data_dir,
        "load_data": False,
        "data_gen_planner": "pyperplan",
        "data_gen_method": "planning",
        "planning_timeout": 10,
    })
    # Cover cases where approach is None or invalid.
    plan_sequence = [None, []]
    approach = _MockApproach(plan_sequence)
    assert approach.get_name() == "dummy"
    env = create_env("pyperplan-blocks")
    _run_pipeline(approach, env)
    # Run again but with data loading.
    utils.reset_flags({
        "env": "pyperplan-blocks",
        "approach": "dummy",
        "experiment_id": "dummy",
        "num_train_tasks": 1,
        "num_eval_tasks": 2,
        "train_task_offset": 0,
        "results_dir": temp_results_dir,
        "data_dir": temp_data_dir,
        "load_data": True,
        "data_gen_planner": "pyperplan",
        "data_gen_method": "planning",
        "planning_timeout": 10,
    })
    plan_sequence = [None, []]
    approach = _MockApproach(plan_sequence)
    _run_pipeline(approach, env)
    # Remove temporary dirs.
    shutil.rmtree(temp_results_dir)
    shutil.rmtree(temp_data_dir)


def test_run_evaluation():
    """Tests for _run_evaluation() in main.py."""
    utils.reset_flags({
        "num_train_tasks": 0,
        "num_eval_tasks": 2,
        "train_task_offset": 0,
    })
    # Cover cases where approach is None or invalid.
    plan_sequence = [None, []]
    approach = _MockApproach(plan_sequence)
    assert approach.get_name() == "dummy"
    env_name = "pyperplan-blocks"
    env = create_env(env_name)
    eval_tasks = env.get_eval_tasks()
    results = _run_evaluation(approach, eval_tasks)
    assert len(results) == 2
    task0_id, task1_id = sorted(results)
    assert results[task0_id]["result"] == "no_plan_found"
    assert results[task1_id]["result"] == "invalid_plan"
