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
                            stop_token,
                            num_completions=1):
        responses = []
        prompt_info = {
            "temperature": temperature,
            "seed": seed,
            "num_completions": num_completions,
            "stop_token": stop_token,
        }
        for _ in range(num_completions):
            text = (f"Prompt was: {prompt}. Seed: {seed}. "
                    f"Temp: {temperature:.1f}.")
            tokens = [text]
            logprobs = [0.0]
            other_info = {"dummy": 0}
            response = LLMResponse(prompt, text, tokens, logprobs,
                                   prompt_info.copy(), other_info)
            responses.append(response)
        return responses


def test_large_language_model():
    """Tests for LargeLanguageModel()."""
    cache_dir = "_fake_llm_cache_dir"
    utils.reset_flags({
        "llm_cache_dir": cache_dir,
        "llm_use_cache_only": False,
        "llm_max_total_tokens": 700
    })
    # Remove the fake cache dir in case it's lying around from old tests.
    shutil.rmtree(cache_dir, ignore_errors=True)
    # Query a dummy LLM.
    llm = _DummyLLM()
    assert llm.get_id() == "dummy"
    responses = llm.sample_completions("Hello world!", 0.5, 123, "", 3)
    completions = [r.response_text for r in responses]
    expected_completion = "Prompt was: Hello world!. Seed: 123. Temp: 0.5."
    assert completions == [expected_completion] * 3
    # Query it again, covering the case where we load from disk.
    responses = llm.sample_completions("Hello world!", 0.5, 123, "", 3)
    completions = [r.response_text for r in responses]
    assert completions == [expected_completion] * 3
    # Query with temperature 0.
    responses = llm.sample_completions("Hello world!", 0.0, 123, "", 3)
    completions = [r.response_text for r in responses]
    expected_completion = "Prompt was: Hello world!. Seed: 123. Temp: 0.0."
    assert completions == [expected_completion] * 3
    # Clean up the cache dir.
    shutil.rmtree(cache_dir)
    # Test llm_use_cache_only.
    utils.reset_flags({
        "llm_cache_dir": cache_dir,
        "llm_use_cache_only": True,
        "llm_max_total_tokens": 700
    })
    with pytest.raises(ValueError) as e:
        completions = llm.sample_completions("Hello world!", 0.5, 123, "", 3)
    assert "No cached response found for LLM prompt." in str(e)


def test_openai_llm():
    """Tests for OpenAILLM()."""
    cache_dir = "_fake_llm_cache_dir"
    utils.reset_flags({
        "llm_cache_dir": cache_dir,
        "llm_use_cache_only": False,
        "llm_max_total_tokens": 700
    })
    if "OPENAI_API_KEY" not in os.environ:  # pragma: no cover
        os.environ["OPENAI_API_KEY"] = "dummy API key"
    # Create an OpenAILLM with the curie model.
    llm = OpenAILLM("text-curie-001")
    assert llm.get_id() == "openai-text-curie-001"
    # Uncomment this to test manually, but do NOT uncomment in master, because
    # each query costs money.
    # completions = llm.sample_completions("Hello", 0.5, 123, "", 2)
    # assert len(completions) == 2
    # completions2 = llm.sample_completions("Hello", 0.5, 123, "", 2)
    # assert completions == completions2
    # shutil.rmtree(cache_dir)

    # Test _raw_to_llm_response().
    raw_response = {
        "text": "Hello world",
        "logprobs": {
            "tokens": ["Hello", "world"],
            "token_logprobs": [-1.0, -2.0]
        }
    }
    prompt = "Dummy prompt"
    temperature = 0.5
    seed = 123
    num_completions = 1
    stop_token = "Q:"
    llm_response = llm._raw_to_llm_response(  # pylint: disable=protected-access
        raw_response, prompt, temperature, seed, stop_token, num_completions)
    assert llm_response.prompt_text == "Dummy prompt"
    assert llm_response.response_text == "Hello world"
    assert llm_response.tokens == ["Hello", "world"]
    assert llm_response.token_logprobs == [-1.0, -2.0]
    assert llm_response.prompt_info["temperature"] == temperature
    assert llm_response.prompt_info["seed"] == seed
    assert llm_response.prompt_info["num_completions"] == num_completions
    assert llm_response.prompt_info["stop_token"] == stop_token
