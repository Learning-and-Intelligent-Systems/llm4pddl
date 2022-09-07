"""Test cases for LLM approaches."""

import shutil
from typing import List

import numpy as np
import pytest
from sentence_transformers import SentenceTransformer
from sentence_transformers.util import cos_sim

from llm4pddl import utils
from llm4pddl.approaches import create_approach
from llm4pddl.approaches.llm_open_loop_approach import LLMOpenLoopApproach
from llm4pddl.dataset import create_dataset
from llm4pddl.envs import create_env
from llm4pddl.llm_interface import LargeLanguageModel
from llm4pddl.structs import Datum, LLMResponse

# Create a mock LLM so that we can control the outputs.


class _MockLLM(LargeLanguageModel):

    def __init__(self):
        self.responses = []

    def get_id(self):
        responses = "-".join(self.responses)
        return f"dummy-{hash(responses)}"

    def _sample_completions(self,
                            prompt,
                            temperature,
                            seed,
                            stop_token,
                            num_completions=1):
        del prompt, temperature, seed, num_completions  # unused
        if not self.responses:
            return []
        next_response = self.responses.pop(0)
        if stop_token in next_response:
            next_response, _ = next_response.split(stop_token, 1)
        response = LLMResponse("", next_response, [], [], {}, {})
        return [response]

    def sample_completions(self,
                           prompt: str,
                           temperature: float,
                           seed: int,
                           stop_token: str,
                           num_completions: int = 1,
                           disable_cache: bool = False) -> List[LLMResponse]:
        # Always disable the cache for tests.
        del disable_cache
        return super().sample_completions(prompt,
                                          temperature,
                                          seed,
                                          stop_token,
                                          num_completions,
                                          disable_cache=True)


@pytest.mark.parametrize(
    'env_name',
    ["pyperplan-blocks", "custom-easy_spanner", "pyperplan-woodworking"])
def test_llm_standard_approach(env_name):
    """Tests for the LLM standard approach."""
    cache_dir = "_fake_llm_cache_dir"
    data_dir = "_fake_data_dir"
    utils.reset_flags({
        "llm_cache_dir": cache_dir,
        "num_train_tasks": 1,
        "num_eval_tasks": 1,
        "train_task_offset": 0,
        "llm_model_name": "code-davinci-002",  # should not matter for test
        "llm_use_cache_only": False,
        "llm_max_total_tokens": 700,
        "llm_prompt_method": "standard",
        "planner": "pyperplan",
        "data_gen_planner": "pyperplan",
        "data_gen_method": "planning",
        "planning_timeout": 100,
        "llm_prompt_flatten_pddl": False,
        "llm_autoregressive_prompting": False,
        "use_dynamic_examples": False,
        "data_dir": data_dir,
        "load_data": False,
        "embedding_model_name": "paraphrase-MiniLM-L6-v2"
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
    plan, _ = utils.run_planning(task)
    ideal_response = "\n".join(plan)
    # Add an empty line to the ideal response, should be no problem.
    ideal_response = "\n" + ideal_response
    llm.responses = [ideal_response]
    # Run the approach.
    plan, _ = approach.solve(task)
    assert utils.validate_plan(task, plan)

    shutil.rmtree(cache_dir)
    shutil.rmtree(data_dir)


def test_autoregressive_prompting():
    """Tests for the LLM standard approach with autoregressive prompting."""
    cache_dir = "_fake_llm_cache_dir"
    data_dir = "_fake_data_dir"
    env_name = "pyperplan-blocks"
    utils.reset_flags({
        "llm_cache_dir": cache_dir,
        "num_train_tasks": 1,
        "num_eval_tasks": 1,
        "train_task_offset": 0,
        "llm_model_name": "code-davinci-002",  # should not matter for test
        "llm_use_cache_only": False,
        "llm_max_total_tokens": 700,
        "llm_prompt_method": "standard",
        "planner": "pyperplan",
        "data_gen_planner": "pyperplan",
        "data_gen_method": "planning",
        "planning_timeout": 100,
        "llm_prompt_flatten_pddl": False,
        "llm_autoregressive_prompting": True,  # note
        "llm_autoregress_max_loops": 25,
        "use_dynamic_examples": False,
        "data_dir": data_dir,
        "load_data": False,
        "embedding_model_name": "paraphrase-MiniLM-L6-v2"
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
    ideal_plan, _ = utils.run_planning(task)
    llm.responses = list(ideal_plan)
    plan, _ = approach.solve(task)
    assert utils.validate_plan(task, plan)
    # Test successful usage, where the LLM output is very close to a plan.
    llm.responses = list(ideal_plan)
    assert llm.responses[0] == "(unstack b c)"
    llm.responses[0] = "(unstck b c)"
    plan, _ = approach.solve(task)
    assert plan[0] == "(unstack b c)"
    assert utils.validate_plan(task, plan)
    # Test failure, where the LLM output is trivial.
    llm.responses = [f"\n{utils.LLM_QUESTION_TOKEN} garbage"]
    plan, _ = approach.solve(task)
    assert plan is None
    # Test failure, where the LLM output is insufficient.
    llm.responses = [ideal_plan[0][:-1]]
    plan, _ = approach.solve(task)
    assert plan is None
    shutil.rmtree(cache_dir)
    shutil.rmtree(data_dir)


@pytest.mark.parametrize("llm_prompt_method",
                         ["standard", "group-by-predicate"])
def test_llm_standard_approach_failure_cases(llm_prompt_method):
    """Tests failure cases for the LLM standard approach."""
    cache_dir = "_fake_llm_cache_dir"
    data_dir = "_fake_data_dir"
    utils.reset_flags({
        "llm_cache_dir": cache_dir,
        "num_train_tasks": 1,
        "num_eval_tasks": 1,
        "train_task_offset": 0,
        "llm_model_name": "code-davinci-002",  # should not matter for test
        "llm_use_cache_only": False,
        "llm_max_total_tokens": 700,
        "llm_multi_num_completions": 5,
        "llm_multi_temperature": 0.5,
        "llm_prompt_method": llm_prompt_method,
        "llm_autoregressive_prompting": False,
        "planner": "pyperplan",
        "data_gen_planner": "pyperplan",
        "data_gen_method": "planning",
        "planning_timeout": 100,
        "llm_prompt_flatten_pddl": False,
        "use_dynamic_examples": False,
        "data_dir": data_dir,
        "load_data": False,
        "embedding_model_name": "paraphrase-MiniLM-L6-v2"
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
    ideal_plan, _ = utils.run_planning(task)
    ideal_response = "\n".join(ideal_plan)

    # Test general approach failure.
    llm.responses = ["garbage"]
    plan, _ = approach.solve(task)
    assert plan is None

    # Test failure cases of _llm_response_to_plan().
    assert approach._llm_response_to_plan(ideal_response, task)  # pylint: disable=protected-access
    # Cases where a line contains malformed parentheses.
    response = "()\n" + ideal_response  # should be skipped
    plan = approach._llm_response_to_plan(response, task)  # pylint: disable=protected-access
    assert len(plan) == len(ideal_plan)
    response = ")(\n" + ideal_response  # should not parse any plan
    plan = approach._llm_response_to_plan(response, task)  # pylint: disable=protected-access
    assert not plan
    # Case where there is an unmatched left parenthesis.
    response = ideal_response + "\n("  # should be skipped
    plan = approach._llm_response_to_plan(response, task)  # pylint: disable=protected-access
    assert len(plan) == len(ideal_plan)
    # Case where object names are incorrect.
    assert "(up f0 f1)" in ideal_response
    response = ideal_response.replace("(up f0 f1)", "(up dummy f1)")
    plan = approach._llm_response_to_plan(response, task)  # pylint: disable=protected-access
    assert len(plan) == len(ideal_plan) - 1
    # Case where operator names are incorrect.
    response = ideal_response.replace("(up f0 f1)", "(up-dummy f0 f1)")
    plan = approach._llm_response_to_plan(response, task)  # pylint: disable=protected-access
    assert len(plan) == len(ideal_plan) - 1
    # Cases where the type signature of the operator is wrong.
    response = ideal_response.replace("(up f0 f1)", "(up f0)")
    plan = approach._llm_response_to_plan(response, task)  # pylint: disable=protected-access
    assert len(plan) == len(ideal_plan) - 1
    response = ideal_response.replace("(up f0 f1)", "(up p0 f1)")
    plan = approach._llm_response_to_plan(response, task)  # pylint: disable=protected-access
    assert len(plan) == len(ideal_plan) - 1
    response = ideal_response.replace("(up f0 f1)", "(up f0 f1 f1)")
    plan = approach._llm_response_to_plan(response, task)  # pylint: disable=protected-access
    assert len(plan) == len(ideal_plan) - 1

    shutil.rmtree(cache_dir)
    shutil.rmtree(data_dir)


def test_llm_standard_approach_dynamic_small_example():
    """Test for LLM standard approach using dynamic examples."""
    cache_dir = "_fake_llm_cache_dir"
    llm = _MockLLM()
    llm.responses = ["doesnt matter"]
    dataset = [
        Datum(
            utils.get_task_from_dir(utils.CUSTOM_BENCHMARK_DIR / 'dressed', 1),
            ['Insert plan here'])
    ]
    utils.reset_flags({
        "llm_cache_dir": cache_dir,
        "num_train_tasks": 1,
        "num_eval_tasks": 1,
        "llm_model_name": "code-davinci-002",
        "llm_max_total_tokens": 700,
        "llm_multi_temperature": 0.3,
        "llm_prompt_method": "standard",
        "llm_autoregressive_prompting": False,
        "planning_timeout": 100,
        "llm_prompt_flatten_pddl": True,
        "use_dynamic_examples": False,  # this is the only one that differs
        "embedding_model_name": "paraphrase-MiniLM-L6-v2",
        "llm_use_cache_only": False
    })
    non_dynamic_approach = create_approach("llm-standard")
    non_dynamic_approach._llm = llm  # pylint: disable=protected-access
    non_dynamic_approach.train(dataset)

    utils.reset_flags({
        "llm_cache_dir": cache_dir,
        "num_train_tasks": 1,
        "num_eval_tasks": 1,
        "llm_model_name": "code-davinci-002",
        "llm_max_total_tokens": 700,
        "llm_multi_temperature": 0.3,
        "llm_prompt_method": "standard",
        "llm_autoregressive_prompting": False,
        "planning_timeout": 100,
        "llm_prompt_flatten_pddl": True,
        "use_dynamic_examples": True,  # this is the only one that differs
        "embedding_model_name": "paraphrase-MiniLM-L6-v2",
        "llm_use_cache_only": False
    })
    dynamic_approach = create_approach("llm-standard")
    dynamic_approach._llm = llm  # pylint: disable=protected-access
    dynamic_approach.train(dataset)

    assert len(dynamic_approach._list_embeddings_mapping) == 1  # pylint: disable=protected-access
    # since training num is 1, these should be the same:
    assert (dynamic_approach._prompt_prefix ==  # pylint: disable=protected-access
            non_dynamic_approach._prompt_prefix)  # pylint: disable=protected-access
    dynamic_approach.solve(
        utils.get_task_from_dir(utils.CUSTOM_BENCHMARK_DIR / 'dressed', 1))
    assert (dynamic_approach._prompt_prefix ==  # pylint: disable=protected-access
            non_dynamic_approach._prompt_prefix)  # pylint: disable=protected-access


def test_llm_standard_approach_dynamic_big_example():
    """Test for LLM standard approach using dynamic examples."""
    cache_dir = "_fake_llm_cache_dir"
    llm = _MockLLM()
    llm.responses = ["doesnt matter"]
    dataset = [
        Datum(
            utils.get_task_from_dir(utils.PYPERPLAN_BENCHMARK_DIR / 'blocks',
                                    i), ['insert plan here'])
        for i in range(2, 32)
    ]
    utils.reset_flags({
        "llm_cache_dir": cache_dir,
        "num_train_tasks": 30,
        "num_eval_tasks": 1,
        "llm_model_name": "code-davinci-002",
        "llm_max_total_tokens": 700,
        "llm_multi_temperature": 0.3,
        "llm_prompt_method": "standard",
        "llm_autoregressive_prompting": False,
        "planning_timeout": 100,
        "llm_prompt_flatten_pddl": True,
        "use_dynamic_examples": False,  # this is the only one that differs
        "embedding_model_name": "paraphrase-MiniLM-L6-v2",
        "llm_use_cache_only": False
    })
    non_dynamic_approach = create_approach("llm-standard")
    non_dynamic_approach._llm = llm  # pylint: disable=protected-access
    non_dynamic_approach.train(dataset)

    utils.reset_flags({
        "llm_cache_dir": cache_dir,
        "num_train_tasks": 30,
        "num_eval_tasks": 1,
        "llm_model_name": "code-davinci-002",
        "llm_max_total_tokens": 700,
        "llm_multi_temperature": 0.3,
        "llm_prompt_method": "standard",
        "llm_autoregressive_prompting": False,
        "planning_timeout": 100,
        "llm_prompt_flatten_pddl": True,
        "use_dynamic_examples": True,  # this is the only one that differs
        "embedding_model_name": "paraphrase-MiniLM-L6-v2",
        "llm_use_cache_only": False
    })
    dynamic_approach = create_approach("llm-standard")
    dynamic_approach._llm = llm  # pylint: disable=protected-access
    dynamic_approach.train(dataset)
    dynamic_approach.solve(
        utils.get_task_from_dir(utils.PYPERPLAN_BENCHMARK_DIR / 'blocks', 1))

    assert len(non_dynamic_approach._list_embeddings_mapping) == 0  # pylint: disable=protected-access
    assert len(dynamic_approach._list_embeddings_mapping) != 0  # pylint: disable=protected-access
    # it is recognized (via trial and error) that the order
    # of the prompts should change:
    assert (non_dynamic_approach._prompt_prefix !=  # pylint: disable=protected-access
            dynamic_approach._prompt_prefix)  # pylint: disable=protected-access
    # however, length should be the same, since only order is changed:
    assert len(non_dynamic_approach._prompt_prefix) == len(  # pylint: disable=protected-access
        dynamic_approach._prompt_prefix)  # pylint: disable=protected-access


def test_llm_multi_approach():
    """Tests for the LLM multi approach."""
    cache_dir = "_fake_llm_cache_dir"
    utils.reset_flags({
        "llm_cache_dir": cache_dir,
        "num_train_tasks": 1,
        "num_eval_tasks": 1,
        "train_task_offset": 0,
        "llm_model_name": "code-davinci-002",  # should not matter for test
        "llm_max_total_tokens": 700,
        "llm_multi_temperature": 0.3,
        "llm_multi_num_completions": 3,
        "llm_prompt_method": "standard",
        "llm_autoregressive_prompting": False,
        "llm_prompt_flatten_pddl": False,
        "embedding_model_name": "paraphrase-MiniLM-L6-v2"
    })
    approach = create_approach("llm-multi")
    assert approach.get_name() == "llm-open-loop"
    assert approach.is_learning_based
    assert not approach.is_planning_based
    assert approach._num_completions == 3  # pylint: disable=protected-access
    assert approach._temperature == 0.3  # pylint: disable=protected-access


def test_embed_tasks():
    """Tests for embed_tasks()."""
    utils.reset_flags({
        "embedding_model_name": "paraphrase-MiniLM-L6-v2",
        "llm_prompt_flatten_pddl": True,
        "llm_model_name": "davinci-002",
        "llm_prompt_method": "standard",
        "llm_autoregressive_prompting": False,
    })
    approach: LLMOpenLoopApproach = create_approach('llm-standard')
    tasks = [
        utils.get_task_from_dir(utils.CUSTOM_BENCHMARK_DIR / 'dressed', i)
        for i in range(1, 2)
    ]
    for j, emb in enumerate(approach._embed_tasks(tasks)):  # pylint: disable=protected-access
        assert np.all(emb['init'] == approach._embed_task(  # pylint: disable=protected-access
            utils.get_task_from_dir(utils.CUSTOM_BENCHMARK_DIR / 'dressed', j +
                                    1))['init'])
        assert np.all(emb['goal'] == approach._embed_task(  # pylint: disable=protected-access
            utils.get_task_from_dir(utils.CUSTOM_BENCHMARK_DIR / 'dressed', j +
                                    1))['goal'])


def test_embed_task():
    """Tests for embed_task()."""
    utils.reset_flags({
        "embedding_model_name": "paraphrase-MiniLM-L6-v2",
        "llm_prompt_flatten_pddl": True,
        "llm_model_name": "davinci-002",
        "llm_prompt_method": "standard",
        "llm_autoregressive_prompting": False,
    })
    approach: LLMOpenLoopApproach = create_approach('llm-standard')
    embedding_model = SentenceTransformer("paraphrase-MiniLM-L6-v2")
    task01 = utils.get_task_from_dir(utils.CUSTOM_BENCHMARK_DIR / 'dressed', 1)
    embedding1 = approach._embed_task(task01)  # pylint: disable=protected-access
    goal_string = utils.get_goal_str(task01)
    init_string = utils.get_init_str(task01)
    goal_embedding2 = embedding_model.encode(goal_string)
    init_embedding2 = embedding_model.encode(init_string)
    assert np.all(embedding1['goal'] == goal_embedding2)
    assert np.all(embedding1['init'] == init_embedding2)


def test_make_embeddings_mapping():
    """Tests make_embeddings_mapping()."""
    utils.reset_flags({
        "llm_model_name": "davinci-002",
        "embedding_model_name": "paraphrase-MiniLM-L6-v2"
    })
    approach: LLMOpenLoopApproach = create_approach('llm-standard')
    embeddings = [[0.5], [0.1], [0.2]]
    embeddings = [{
        'init': [0.5],
        'goal': [0]
    }, {
        'init': [0.1],
        'goal': [0]
    }, {
        'init': [0.2],
        'goal': [0.3]
    }]
    tasks = [
        utils.get_task_from_dir(utils.CUSTOM_BENCHMARK_DIR / 'dressed', i)
        for i in range(1, 4)
    ]
    dataset = [Datum(task, ['insert plan here']) for task in tasks]
    mapping = approach._make_embeddings_mapping(embeddings, dataset)  # pylint: disable=protected-access
    assert len(mapping) == 3
    assert mapping[0]['init_emb'] == [0.5]
    assert mapping[1]['init_emb'] == [0.1]
    assert mapping[2]['goal_emb'] == [0.3]
    assert mapping[0]['datum'].solution == ['insert plan here']


def test_get_closest_datums():
    """Tests for get_closest_datums()."""
    utils.reset_flags({
        "llm_prompt_flatten_pddl": True,
        "embedding_model_name": "paraphrase-MiniLM-L6-v2",
        "llm_model_name": "davinci-002",
        "llm_prompt_method": "standard",
        "llm_autoregressive_prompting": False,
    })
    approach: LLMOpenLoopApproach = create_approach('llm-standard')
    dressed01 = utils.get_task_from_dir(utils.CUSTOM_BENCHMARK_DIR / 'dressed',
                                        1)
    tasks = [
        utils.get_task_from_dir(utils.CUSTOM_BENCHMARK_DIR / 'dressed', i)
        for i in range(2, 5)
    ]
    blocks01 = utils.get_task_from_dir(
        utils.PYPERPLAN_BENCHMARK_DIR / 'blocks', 1)
    blocks02 = utils.get_task_from_dir(
        utils.PYPERPLAN_BENCHMARK_DIR / 'blocks', 2)
    depot01 = utils.get_task_from_dir(utils.PYPERPLAN_BENCHMARK_DIR / 'depot',
                                      1)
    tasks.append(blocks01)
    embeddings = [
        approach._embed_task(task) for task in tasks  # pylint: disable=protected-access
    ]
    dataset = [Datum(task, ['insert plan here']) for task in tasks]
    embeddings_mapping = approach._make_embeddings_mapping(embeddings, dataset)  # pylint: disable=protected-access
    # checking correct output size
    most_similar = approach._get_closest_datums(  # pylint: disable=protected-access
        dressed01, embeddings_mapping, 1)
    assert len(most_similar) == 1
    most_similar2 = approach._get_closest_datums(  # pylint: disable=protected-access
        dressed01, embeddings_mapping, 3)
    assert len(most_similar2) == 3
    most_similar3 = approach._get_closest_datums(  # pylint: disable=protected-access
        dressed01, embeddings_mapping, 4)
    assert len(most_similar3) == 4
    # checking that blocks is the least likely:
    assert most_similar3[0].task == utils.get_task_from_dir(
        utils.PYPERPLAN_BENCHMARK_DIR / 'blocks', 1)
    dif_tasks = [dressed01, blocks01, depot01]
    dif_embeddings = [
        approach._embed_task(task) for task in dif_tasks  # pylint: disable=protected-access
    ]
    dif_dataset = [Datum(task, ['insert plan here']) for task in dif_tasks]
    dif_emb_map = approach._make_embeddings_mapping(  # pylint: disable=protected-access
        dif_embeddings, dif_dataset)
    most_sim1 = approach._get_closest_datums(blocks02, dif_emb_map, 1)  # pylint: disable=protected-access
    # checking that blocks is the most likely of the 3:
    assert most_sim1[0].task == utils.get_task_from_dir(
        utils.PYPERPLAN_BENCHMARK_DIR / 'blocks', 1)
    # big example selecting the correct tasks each time:
    dressed = [
        utils.get_task_from_dir(utils.CUSTOM_BENCHMARK_DIR / 'dressed', i)
        for i in range(2, 5)
    ]
    depot = [
        utils.get_task_from_dir(utils.PYPERPLAN_BENCHMARK_DIR / 'depot', i)
        for i in range(2, 5)
    ]
    blocks = [
        utils.get_task_from_dir(utils.PYPERPLAN_BENCHMARK_DIR / 'blocks', i)
        for i in range(2, 5)
    ]
    big_tasks = dressed + depot + blocks
    big_embeddings = [
        approach._embed_task(task) for task in big_tasks  # pylint: disable=protected-access
    ]
    big_dataset = [Datum(task, ['insert plan here']) for task in big_tasks]
    big_emb_map = approach._make_embeddings_mapping(  # pylint: disable=protected-access
        big_embeddings, big_dataset)
    # comparing to dressed:
    most_similar_dressed = approach._get_closest_datums(  # pylint: disable=protected-access
        dressed01, big_emb_map, 9)
    assert len(most_similar_dressed) == len(big_tasks)
    for datum in most_similar_dressed[-3:]:
        assert datum.task in dressed

    # comparing to blocks:
    most_similar_blocks = approach._get_closest_datums(  # pylint: disable=protected-access
        blocks01, big_emb_map, 9)
    for datum in most_similar_blocks[-3:]:
        assert datum.task in blocks

    # comparing to depot:
    most_similar_depot = approach._get_closest_datums(depot01, big_emb_map, 9)  # pylint: disable=protected-access
    for datum in most_similar_depot[-3:]:
        assert datum.task in depot

    # proving identical is considered best:
    most_sim = approach._get_closest_datums(blocks02, big_emb_map, 9)[-1]  # pylint: disable=protected-access
    assert most_sim.task == utils.get_task_from_dir(
        utils.PYPERPLAN_BENCHMARK_DIR / 'blocks', 2)
    # example to compare within a specific domain.
    dif_blocks_tasks = [
        utils.get_task_from_dir(utils.PYPERPLAN_BENCHMARK_DIR / 'blocks', 3),
        utils.get_task_from_dir(utils.PYPERPLAN_BENCHMARK_DIR / 'blocks', 35)
    ]
    dif_blocks_embeddings = [
        approach._embed_task(task)  # pylint: disable=protected-access
        for task in dif_blocks_tasks
    ]
    dif_blocks_dataset = [
        Datum(task, ['insert plan here']) for task in dif_blocks_tasks
    ]
    dif_blocks_emb_map = approach._make_embeddings_mapping(  # pylint: disable=protected-access
        dif_blocks_embeddings, dif_blocks_dataset)
    # Comparing blocks03 and blocks35 in their similarity to blocks01.
    # Heuristically, blocks03 should be considered more similar.
    most_sim_blocks_datum = approach._get_closest_datums(  # pylint: disable=protected-access
        blocks01, dif_blocks_emb_map, 1)[0]
    assert most_sim_blocks_datum.task == utils.get_task_from_dir(
        utils.PYPERPLAN_BENCHMARK_DIR / 'blocks', 3)


def test_get_cosine_sim():
    """Tests get_cosine_sim()."""
    utils.reset_flags({
        "llm_model_name": "davinci-002",
        "embedding_model_name": "paraphrase-MiniLM-L6-v2"
    })
    approach: LLMOpenLoopApproach = create_approach('llm-standard')
    embedding_model = SentenceTransformer("paraphrase-MiniLM-L6-v2")
    embedding1 = embedding_model.encode('hello')
    embedding2 = embedding_model.encode('hello')
    cos_sim1 = approach._get_cosine_sim(embedding1, embedding2)  # pylint: disable=protected-access
    # cos_sim1 should be 1.
    assert abs(cos_sim1 - 1) < 0.00001
    embedding3 = embedding_model.encode('hell')
    cos_sim2 = approach._get_cosine_sim(embedding1, embedding3)  # pylint: disable=protected-access
    # cos_sim2 should not be 1.
    assert cos_sim2 != 1
    embedding4 = embedding_model.encode('my name is')
    embedding5 = embedding_model.encode('my dog is here')
    cos_sim3 = approach._get_cosine_sim(embedding4, embedding5)  # pylint: disable=protected-access
    assert cos_sim3 == cos_sim(embedding4, embedding5).item()
