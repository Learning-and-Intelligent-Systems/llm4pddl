"""Tests for the approaches module."""

import pytest

from llm4pddl import utils
from llm4pddl.approaches import create_approach


def test_create_approach():
    """Tests for create_approach()."""
    utils.reset_flags({
        "llm_model_name": "code-davinci-002",  # should not matter for test
        "llm_use_cache_only": False,
        "llm_max_total_tokens": 700,
        "llm_multi_num_completions": 5,
        "llm_multi_temperature": 0.5,
        "embedding_model_name": "paraphrase-MiniLM-L6-v2"
    })
    approach = create_approach("pure-planning")
    assert approach.get_name() == "pure-planning"
    approach = create_approach("llm-standard")
    assert approach.get_name() == "llm-open-loop"
    approach = create_approach("llm-multi")
    assert approach.get_name() == "llm-open-loop"
    approach = create_approach("llm-standard-plan")
    assert approach.get_name() == "llm-plan"
    approach = create_approach("llm-multi-plan")
    assert approach.get_name() == "llm-plan"
    approach = create_approach("manual-planning")
    assert approach.get_name() == "manual-planning"
    approach = create_approach("random-actions")
    assert approach.get_name() == "random-actions"
    # Test unrecognized approach.
    with pytest.raises(NotImplementedError) as e:
        create_approach("not a real approach")
    assert "Unrecognized approach" in str(e)
