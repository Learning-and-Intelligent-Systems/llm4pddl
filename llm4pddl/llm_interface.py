"""Interface to pretrained large language models."""

import abc
import logging
import os
import pickle
import time
from pathlib import Path
from typing import Any, Dict, List

import openai
from transformers import GPT2TokenizerFast

from llm4pddl import utils
from llm4pddl.flags import FLAGS
from llm4pddl.structs import LLMResponse

# Turn off a warning about parallelism.
# See https://stackoverflow.com/questions/62691279
os.environ["TOKENIZERS_PARALLELISM"] = "false"


class LargeLanguageModel(abc.ABC):
    """A pretrained large language model."""

    @abc.abstractmethod
    def get_id(self) -> str:
        """Get a string identifier for this LLM.

        This identifier should include sufficient information so that
        querying the same model with the same prompt and same identifier
        should yield the same result (assuming temperature 0).
        """
        raise NotImplementedError("Override me!")

    @abc.abstractmethod
    def _sample_completions(self,
                            prompt: str,
                            temperature: float,
                            seed: int,
                            stop_token: str,
                            num_completions: int = 1) -> List[LLMResponse]:
        """This is the main method that subclasses must implement.

        This helper method is called by sample_completions(), which
        caches the prompts and responses to disk.
        """
        raise NotImplementedError("Override me!")

    def sample_completions(self,
                           prompt: str,
                           temperature: float,
                           seed: int,
                           stop_token: str,
                           num_completions: int = 1) -> List[LLMResponse]:
        """Sample one or more completions from a prompt.

        Higher temperatures will increase the variance in the responses.
        The seed may not be used and the results may therefore not be
        reproducible for LLMs where we only have access through an API
        that does not expose the ability to set a random seed. Responses
        are saved to disk.
        """
        # Set up the cache file.
        os.makedirs(FLAGS.llm_cache_dir, exist_ok=True)
        llm_id = self.get_id()
        prompt_id = utils.str_to_identifier(prompt)
        # If the temperature is 0, the seed does not matter.
        if temperature == 0.0:
            config_id = f"most_likely_{num_completions}_{stop_token}"
        else:
            config_id = f"{temperature}_{seed}_{num_completions}_{stop_token}"
        cache_filename = f"{llm_id}_{config_id}_{prompt_id}.pkl"
        cache_filepath = Path(FLAGS.llm_cache_dir) / cache_filename
        if not os.path.exists(cache_filepath):
            if FLAGS.llm_use_cache_only:
                raise ValueError("No cached response found for LLM prompt.")
            logging.debug(f"Querying LLM {llm_id} with new prompt.")
            # Query the LLM.
            completions = self._sample_completions(prompt, temperature, seed,
                                                   stop_token, num_completions)
            # Cache the completions.
            with open(cache_filepath, 'wb') as f:
                pickle.dump(completions, f)
            logging.debug(f"Saved LLM response to {cache_filepath}.")
        # Load the saved completion.
        with open(cache_filepath, 'rb') as f:
            completions = pickle.load(f)
        logging.debug(f"Loaded LLM response from {cache_filepath}.")
        return completions


class OpenAILLM(LargeLanguageModel):
    """Interface to openAI LLMs (GPT-3).

    Assumes that an environment variable OPENAI_API_KEY is set to a
    private API key for beta.openai.com.
    """

    def __init__(self, model_name: str) -> None:
        """See https://beta.openai.com/docs/models/gpt-3 for the list of
        available model names."""
        self._model_name = model_name
        assert "OPENAI_API_KEY" in os.environ
        openai.api_key = os.getenv("OPENAI_API_KEY")
        # Create a tokenizer for counting the number of tokens in the prompts.
        self._tokenizer = GPT2TokenizerFast.from_pretrained("gpt2")

    def get_id(self) -> str:
        return f"openai-{self._model_name}"

    def _sample_completions(
            self,
            prompt: str,
            temperature: float,
            seed: int,
            stop_token: str,
            num_completions: int = 1) -> List[LLMResponse]:  # pragma: no cover
        # Always max out the max tokens to get the longest possible responses.
        num_prompt_tokens = len(self._tokenizer(prompt)["input_ids"])
        # If the prompt is too long, warn and give up.
        max_response_tokens = FLAGS.llm_max_total_tokens - num_prompt_tokens
        if max_response_tokens <= 0:
            logging.warning("Prompt length exceeded token budget, skipping!")
            return []
        # Retry 10 times before giving up. In some rare cases, a particular
        # prompt may always lead to an error.
        for _ in range(10):
            try:
                response = openai.Completion.create(  # type: ignore
                    model=self._model_name,
                    prompt=prompt,
                    temperature=temperature,
                    max_tokens=max_response_tokens,
                    logprobs=1,
                    stop=stop_token,
                    n=num_completions)
                # Successfully queried, so break.
                break
            except (openai.error.RateLimitError,
                    openai.error.APIConnectionError, openai.error.APIError):
                # Wait for 60 seconds if this limit is reached. Hopefully rare.
                time.sleep(60)
        else:
            # If we tried 10 times and still failed, return no responses.
            logging.warning("Max query attempts exceeded, skipping!")
            return []
        assert len(response["choices"]) == num_completions
        return [
            self._raw_to_llm_response(r, prompt, temperature, seed, stop_token,
                                      num_completions)
            for r in response["choices"]
        ]

    @staticmethod
    def _raw_to_llm_response(raw_response: Dict[str, Any], prompt: str,
                             temperature: float, seed: int, stop_token: str,
                             num_completions: int) -> LLMResponse:
        text = raw_response["text"]
        tokens = raw_response["logprobs"]["tokens"]
        token_logprobs = raw_response["logprobs"]["token_logprobs"]
        assert len(tokens) == len(token_logprobs)
        prompt_info = {
            "temperature": temperature,
            "seed": seed,
            "num_completions": num_completions,
            "stop_token": stop_token,
        }
        return LLMResponse(prompt,
                           text,
                           tokens,
                           token_logprobs,
                           prompt_info=prompt_info,
                           other_info=raw_response.copy())
