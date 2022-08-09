"""Interface to pretrained large language models."""

import abc
import logging
import os
import pickle
from pathlib import Path
from typing import List

import openai

from llm4pddl.flags import FLAGS

# TODO: get and cache probabilities


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
                            num_completions: int = 1) -> List[str]:
        """This is the main method that subclasses must implement.

        This helper method is called by sample_completions(), which
        caches the prompts and responses to disk.
        """
        raise NotImplementedError("Override me!")

    def sample_completions(self,
                           prompt: str,
                           temperature: float,
                           seed: int,
                           num_completions: int = 1) -> List[str]:
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
        prompt_id = hash(prompt)
        # If the temperature is 0, the seed does not matter.
        if temperature == 0.0:
            config_id = f"most_likely_{num_completions}"
        else:
            config_id = f"{temperature}_{seed}_{num_completions}"
        cache_filename = f"{llm_id}_{config_id}_{prompt_id}.txt"
        cache_filepath = Path(FLAGS.llm_cache_dir) / cache_filename
        if not os.path.exists(cache_filepath):
            if FLAGS.llm_use_cache_only:
                raise ValueError("No cached response found for LLM prompt.")
            logging.debug(f"Querying LLM {llm_id} with new prompt.")
            # Query the LLM.
            completions = self._sample_completions(prompt, temperature, seed,
                                                   num_completions)
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
        # Note that max_tokens is the maximum response length (not prompt).
        # From OpenAI docs: "The token count of your prompt plus max_tokens
        # cannot exceed the model's context length."
        self._max_tokens = FLAGS.llm_openai_max_response_tokens
        assert "OPENAI_API_KEY" in os.environ
        openai.api_key = os.getenv("OPENAI_API_KEY")

    def get_id(self) -> str:
        return f"openai-{self._model_name}"

    def _sample_completions(
            self,
            prompt: str,
            temperature: float,
            seed: int,
            num_completions: int = 1) -> List[str]:  # pragma: no cover
        del seed  # unused
        response = openai.Completion.create(
            model=self._model_name,  # type: ignore
            prompt=prompt,
            temperature=temperature,
            max_tokens=self._max_tokens,
            n=num_completions)
        assert len(response["choices"]) == num_completions
        text_responses = [
            response["choices"][i]["text"] for i in range(num_completions)
        ]
        return text_responses
