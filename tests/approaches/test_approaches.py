"""Tests for the approaches module."""

import pytest

from llm4pddl.approaches import create_approach


def test_create_approach():
    """Tests for create_approach()."""
    approach = create_approach("pure-planning")
    assert approach.get_name() == "pure-planning"
    # Test unrecognized approach.
    with pytest.raises(NotImplementedError) as e:
        create_approach("not a real approach")
    assert "Unrecognized approach" in str(e)
