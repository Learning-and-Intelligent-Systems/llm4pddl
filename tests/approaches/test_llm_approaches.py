"""Test cases for LLM approaches."""

import shutil

import numpy as np
import pytest

from llm4pddl import utils
from llm4pddl.approaches import create_approach
from llm4pddl.dataset import create_dataset
from llm4pddl.envs import ALL_ENVS, create_env
from llm4pddl.llm_interface import LargeLanguageModel
from llm4pddl.structs import LLMResponse

# Wrap text responses into LLMResponses with dummy entries.
wrap_response = lambda text: LLMResponse("", text, [], [], {}, {})

# Create a mock LLM so that we can control the outputs.


class _MockLLM(LargeLanguageModel):

    def __init__(self):
        self.response = None

    def get_id(self):
        return f"dummy-{hash(self.response)}"

    def _sample_completions(self,
                            prompt,
                            temperature,
                            seed,
                            num_completions=1):
        del prompt, temperature, seed, num_completions  # unused
        response = wrap_response(self.response)
        return [response]


@pytest.mark.parametrize('env_name', ALL_ENVS)
def test_llm_standard_approach(env_name):
    """Tests for the LLM standard approach."""
    cache_dir = "_fake_llm_cache_dir"
    utils.reset_flags({
        "llm_cache_dir": cache_dir,
        "num_train_tasks": 1,
        "num_eval_tasks": 1,
        "llm_model_name": "code-davinci-002",  # should not matter for test
        "llm_use_cache_only": False,
        "llm_openai_max_response_tokens": 700,
        "planner": "pyperplan",
        "planning_timeout": 100,
    })
    env = create_env(env_name)
    train_tasks = env.get_train_tasks()
    approach = create_approach("llm-standard")
    assert approach.get_name() == "llm-open-loop"
    assert approach.is_learning_based
    assert not approach.is_planning_based
    # Test "learning", i.e., constructing the prompt prefix.
    dataset = create_dataset(train_tasks)
    assert not approach._prompt_prefix  # pylint: disable=protected-access
    approach.train(dataset)
    assert approach._prompt_prefix  # pylint: disable=protected-access
    llm = _MockLLM()
    approach._llm = llm  # pylint: disable=protected-access
    # Test successful usage, where the LLM output corresponds to a plan.
    task_idx = 0
    task = train_tasks[task_idx]
    rng = np.random.default_rng(123)
    plan, _ = utils.run_planning(task, rng)
    ideal_response = "\n".join(plan)
    # Add an empty line to the ideal response, should be no problem.
    ideal_response = "\n" + ideal_response
    llm.response = ideal_response
    # Run the approach.
    plan, _ = approach.solve(task)
    assert utils.validate_plan(task, plan)

    shutil.rmtree(cache_dir)


def test_llm_standard_approach_failure_cases():
    """Tests failure cases for the LLM standard approach."""
    cache_dir = "_fake_llm_cache_dir"
    utils.reset_flags({
        "llm_cache_dir": cache_dir,
        "num_train_tasks": 1,
        "num_eval_tasks": 1,
        "llm_model_name": "code-davinci-002",  # should not matter for test
        "llm_use_cache_only": False,
        "llm_openai_max_response_tokens": 700,
        "planner": "pyperplan",
        "planning_timeout": 100,
    })
    env = create_env("pyperplan-miconic")
    train_tasks = env.get_train_tasks()
    approach = create_approach("llm-standard")
    dataset = create_dataset(train_tasks)
    approach.train(dataset)
    llm = _MockLLM()
    approach._llm = llm  # pylint: disable=protected-access
    task_idx = 0
    task = train_tasks[task_idx]
    rng = np.random.default_rng(123)
    plan, _ = utils.run_planning(task, rng)
    ideal_response = "\n".join(plan)

    # Test general approach failure.
    llm.response = "garbage"
    plan, _ = approach.solve(task)
    assert plan is None

    # Test failure cases of _llm_response_to_plan().
    assert approach._llm_response_to_plan(wrap_response(ideal_response), task)  # pylint: disable=protected-access
    # Cases where a line contains malformed parentheses.
    response = "()\n" + ideal_response
    plan = approach._llm_response_to_plan(wrap_response(response), task)  # pylint: disable=protected-access
    assert not plan
    response = ")(\n" + ideal_response
    plan = approach._llm_response_to_plan(wrap_response(response), task)  # pylint: disable=protected-access
    assert not plan
    # Case where object names are incorrect.
    assert "(up f0 f1)" in ideal_response
    response = ideal_response.replace("(up f0 f1)", "(up dummy f1)")
    plan = approach._llm_response_to_plan(wrap_response(response), task)  # pylint: disable=protected-access
    assert not plan
    # Case where operator names are incorrect.
    response = ideal_response.replace("(up f0 f1)", "(up-dummy f0 f1)")
    plan = approach._llm_response_to_plan(wrap_response(response), task)  # pylint: disable=protected-access
    assert not plan
    # Cases where the type signature of the operator is wrong.
    response = ideal_response.replace("(up f0 f1)", "(up f0)")
    plan = approach._llm_response_to_plan(wrap_response(response), task)  # pylint: disable=protected-access
    assert not plan
    response = ideal_response.replace("(up f0 f1)", "(up p0 f1)")
    plan = approach._llm_response_to_plan(wrap_response(response), task)  # pylint: disable=protected-access
    assert not plan
    response = ideal_response.replace("(up f0 f1)", "(up f0 f1 f1)")
    plan = approach._llm_response_to_plan(wrap_response(response), task)  # pylint: disable=protected-access
    assert not plan

    shutil.rmtree(cache_dir)
