"""Tests for main.py."""

import shutil
import sys
import tempfile

from llm4pddl.main import _main


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
