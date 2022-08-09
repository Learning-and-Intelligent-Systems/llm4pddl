"""Tests for the large language model interface."""

import os
import shutil

import pytest

from llm4pddl import utils
from llm4pddl.llm_interface import LargeLanguageModel, OpenAILLM
from llm4pddl.structs import LLMResponse


class _DummyLLM(LargeLanguageModel):

    def get_id(self):
        return "dummy"

    def _sample_completions(self,
                            prompt,
                            temperature,
                            seed,
                            num_completions=1):
        responses = []
        for _ in range(num_completions):
            text = (f"Prompt was: {prompt}. Seed: {seed}. "
                    f"Temp: {temperature:.1f}.")
            tokens = [text]
            logprobs = [0.0]
            additional_info = {"seed": seed}
            response = LLMResponse(text, tokens, logprobs, additional_info)
            responses.append(response)
        return responses


def test_large_language_model():
    """Tests for LargeLanguageModel()."""
    cache_dir = "_fake_llm_cache_dir"
    utils.reset_flags({
        "llm_cache_dir": cache_dir,
        "llm_use_cache_only": False,
        "llm_openai_max_response_tokens": 700
    })
    # Remove the fake cache dir in case it's lying around from old tests.
    shutil.rmtree(cache_dir, ignore_errors=True)
    # Query a dummy LLM.
    llm = _DummyLLM()
    assert llm.get_id() == "dummy"
    responses = llm.sample_completions("Hello world!", 0.5, 123, 3)
    completions = [r.text for r in responses]
    expected_completion = "Prompt was: Hello world!. Seed: 123. Temp: 0.5."
    assert completions == [expected_completion] * 3
    # Query it again, covering the case where we load from disk.
    responses = llm.sample_completions("Hello world!", 0.5, 123, 3)
    completions = [r.text for r in responses]
    assert completions == [expected_completion] * 3
    # Query with temperature 0.
    responses = llm.sample_completions("Hello world!", 0.0, 123, 3)
    completions = [r.text for r in responses]
    expected_completion = "Prompt was: Hello world!. Seed: 123. Temp: 0.0."
    assert completions == [expected_completion] * 3
    # Clean up the cache dir.
    shutil.rmtree(cache_dir)
    # Test llm_use_cache_only.
    utils.reset_flags({
        "llm_cache_dir": cache_dir,
        "llm_use_cache_only": True,
        "llm_openai_max_response_tokens": 700
    })
    with pytest.raises(ValueError) as e:
        completions = llm.sample_completions("Hello world!", 0.5, 123, 3)
    assert "No cached response found for LLM prompt." in str(e)


def test_openai_llm():
    """Tests for OpenAILLM()."""
    cache_dir = "_fake_llm_cache_dir"
    utils.reset_flags({
        "llm_cache_dir": cache_dir,
        "llm_use_cache_only": False,
        "llm_openai_max_response_tokens": 700
    })
    if "OPENAI_API_KEY" not in os.environ:
        os.environ["OPENAI_API_KEY"] = "dummy API key"
    # Create an OpenAILLM with the curie model.
    llm = OpenAILLM("text-curie-001")
    assert llm.get_id() == "openai-text-curie-001"
    # Uncomment this to test manually, but do NOT uncomment in master, because
    # each query costs money.
    # completions = llm.sample_completions("Hello", 0.5, 123, 2)
    # assert len(completions) == 2
    # completions2 = llm.sample_completions("Hello", 0.5, 123, 2)
    # assert completions == completions2
    # shutil.rmtree(cache_dir)
