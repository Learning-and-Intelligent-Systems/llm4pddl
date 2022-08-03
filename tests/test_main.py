"""Tests for main.py."""

import sys

from llm4pddl.main import _main


def test_main():
    """Tests for main.py."""
    sys.argv = ["dummy", "--env", "my_env", "--approach", "my_approach"]
    _main()  # should run
