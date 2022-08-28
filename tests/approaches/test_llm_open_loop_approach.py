"""Test cases for LLM approaches."""

import shutil

import numpy as np
import pytest
from sentence_transformers import SentenceTransformer
from sentence_transformers.util import cos_sim

from llm4pddl import utils
from llm4pddl.approaches import create_approach
from llm4pddl.approaches.llm_open_loop_approach import LLMOpenLoopApproach
from llm4pddl.dataset import create_dataset
from llm4pddl.envs import ALL_ENVS, create_env
from llm4pddl.llm_interface import LargeLanguageModel
from llm4pddl.structs import Datum, LLMResponse

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
        "llm_max_total_tokens": 700,
        "llm_prompt_method": "standard",
        "planner": "pyperplan",
        "data_gen_planner": "pyperplan",
        "planning_timeout": 100,
        "llm_prompt_flatten_pddl": False,
        "use_dynamic_examples": False
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
    llm.response = ideal_response
    # Run the approach.
    plan, _ = approach.solve(task)
    assert utils.validate_plan(task, plan)

    shutil.rmtree(cache_dir)


@pytest.mark.parametrize("llm_prompt_method",
                         ["standard", "group-by-predicate"])
def test_llm_standard_approach_failure_cases(llm_prompt_method):
    """Tests failure cases for the LLM standard approach."""
    cache_dir = "_fake_llm_cache_dir"
    utils.reset_flags({
        "llm_cache_dir": cache_dir,
        "num_train_tasks": 1,
        "num_eval_tasks": 1,
        "llm_model_name": "code-davinci-002",  # should not matter for test
        "llm_use_cache_only": False,
        "llm_max_total_tokens": 700,
        "llm_multi_num_completions": 5,
        "llm_multi_temperature": 0.5,
        "llm_prompt_method": llm_prompt_method,
        "planner": "pyperplan",
        "data_gen_planner": "pyperplan",
        "planning_timeout": 100,
        "llm_prompt_flatten_pddl": False,
        "use_dynamic_examples": False
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
    # Case where there is an unmatched left parenthesis.
    response = ideal_response + "\n("
    plan = approach._llm_response_to_plan(wrap_response(response), task)  # pylint: disable=protected-access
    assert len(plan) == len(ideal_plan)
    response = "()\n" + ideal_response
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


def test_llm_standard_approach_dynamic_small_example():
    """Test for LLM standard approach using dynamic examples."""
    cache_dir = "_fake_llm_cache_dir"
    utils.reset_flags({
        "llm_cache_dir": cache_dir,
        "num_train_tasks": 1,
        "num_eval_tasks": 1,
        "llm_model_name": "code-davinci-002",
        "llm_max_total_tokens": 700,
        "llm_multi_temperature": 0.3,
        # "llm_multi_num_completions": 3,
        "llm_prompt_method": "standard",
        "planning_timeout": 100,
        "llm_prompt_flatten_pddl": True,
        "use_dynamic_examples": False,  # this is the only one that differs
        "embedding_model_name": "paraphrase-MiniLM-L6-v2",
        "llm_use_cache_only": False
    })
    non_dynamic_approach = create_approach("llm-standard")
    utils.reset_flags({
        "llm_cache_dir": cache_dir,
        "num_train_tasks": 1,
        "num_eval_tasks": 1,
        "llm_model_name": "code-davinci-002",
        "llm_max_total_tokens": 700,
        "llm_multi_temperature": 0.3,
        # "llm_multi_num_completions": 3,
        "llm_prompt_method": "standard",
        "planning_timeout": 100,
        "llm_prompt_flatten_pddl": True,
        "use_dynamic_examples": True,  # this is the only one that differs
        "embedding_model_name": "paraphrase-MiniLM-L6-v2",
        "llm_use_cache_only": False
    })
    dynamic_approach = create_approach("llm-standard")
    assert dynamic_approach._list_embeddings_mapping == []  # pylint: disable=protected-access
    dataset = [
        Datum(utils.get_custom_task('dressed', 1), ['Insert plan here'])
    ]
    non_dynamic_approach.train(dataset)
    dynamic_approach.train(dataset)
    assert len(dynamic_approach._list_embeddings_mapping) == 1  # pylint: disable=protected-access
    # since training num is 1, these should be the same:
    assert (dynamic_approach._prompt_prefix ==  # pylint: disable=protected-access
            non_dynamic_approach._prompt_prefix)  # pylint: disable=protected-access
    dynamic_approach.solve(utils.get_custom_task('dressed', 2))
    assert (dynamic_approach._prompt_prefix ==  # pylint: disable=protected-access
            non_dynamic_approach._prompt_prefix)  # pylint: disable=protected-access


def test_llm_standard_approach_dynamic_big_example():
    """Test for LLM standard approach using dynamic examples."""
    cache_dir = "_fake_llm_cache_dir"
    utils.reset_flags({
        "llm_cache_dir": cache_dir,
        "num_train_tasks": 30,
        "num_eval_tasks": 1,
        "llm_model_name": "code-davinci-002",
        "llm_max_total_tokens": 700,
        "llm_multi_temperature": 0.3,
        # "llm_multi_num_completions": 3,
        "llm_prompt_method": "standard",
        "planning_timeout": 100,
        "llm_prompt_flatten_pddl": True,
        "use_dynamic_examples": False,  # this is the only one that differs
        "embedding_model_name": "paraphrase-MiniLM-L6-v2",
        "llm_use_cache_only": False
    })
    non_dynamic_approach = create_approach("llm-standard")
    utils.reset_flags({
        "llm_cache_dir": cache_dir,
        "num_train_tasks": 30,
        "num_eval_tasks": 1,
        "llm_model_name": "code-davinci-002",
        "llm_max_total_tokens": 700,
        "llm_multi_temperature": 0.3,
        # "llm_multi_num_completions": 3,
        "llm_prompt_method": "standard",
        "planning_timeout": 100,
        "llm_prompt_flatten_pddl": True,
        "use_dynamic_examples": True,  # this is the only one that differs
        "embedding_model_name": "paraphrase-MiniLM-L6-v2",
        "llm_use_cache_only": False
    })
    dynamic_approach = create_approach("llm-standard")
    dataset = [
        Datum(utils.get_pyperplan_benchmark_task('blocks', i),
              ['insert plan here']) for i in range(2, 32)
    ]
    non_dynamic_approach.train(dataset)
    dynamic_approach.train(dataset)
    dynamic_approach.solve(utils.get_pyperplan_benchmark_task('blocks', 1))
    assert len(non_dynamic_approach._list_embeddings_mapping) == len(  # pylint: disable=protected-access
        dynamic_approach._list_embeddings_mapping)  # pylint: disable=protected-access
    # they shouldn't be the plan because it is recognized
    # heuristically that the order should change and have questions with a
    # smaller question number closer to the end in the dynamic example
    assert (non_dynamic_approach._prompt_prefix !=  # pylint: disable=protected-access
            dynamic_approach._prompt_prefix)  # pylint: disable=protected-access
    # however, length should be the same, since only order is changed.
    assert len(non_dynamic_approach._prompt_prefix) == len(  # pylint: disable=protected-access
        dynamic_approach._prompt_prefix)  # pylint: disable=protected-access


def test_llm_multi_approach():
    """Tests for the LLM multi approach."""
    cache_dir = "_fake_llm_cache_dir"
    utils.reset_flags({
        "llm_cache_dir": cache_dir,
        "num_train_tasks": 1,
        "num_eval_tasks": 1,
        "llm_model_name": "code-davinci-002",  # should not matter for test
        "llm_max_total_tokens": 700,
        "llm_multi_temperature": 0.3,
        "llm_multi_num_completions": 3,
        "llm_prompt_method": "standard",
        "planning_timeout": 100,
        "llm_prompt_flatten_pddl": False
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
        "llm_prompt_method": "standard"
    })
    approach: LLMOpenLoopApproach = create_approach('llm-standard')
    tasks = [utils.get_custom_task('dressed', i) for i in range(1, 2)]
    embedding_model = SentenceTransformer("paraphrase-MiniLM-L6-v2")
    for j, emb in enumerate(approach.embed_tasks(tasks)):
        assert np.all(emb == approach.embed_task(
            utils.get_custom_task('dressed', j + 1), embedding_model))


def test_embed_task():
    """Tests for embed_task()."""
    utils.reset_flags({
        "embedding_model_name": "paraphrase-MiniLM-L6-v2",
        "llm_prompt_flatten_pddl": True,
        "llm_model_name": "davinci-002",
        "llm_prompt_method": "standard"
    })
    approach: LLMOpenLoopApproach = create_approach('llm-standard')
    embedding_model = SentenceTransformer("paraphrase-MiniLM-L6-v2")
    task01 = utils.get_custom_task('dressed', 1)
    embedding1 = approach.embed_task(task01, embedding_model)
    task_string = approach._create_prompt(task01)  # pylint: disable=protected-access
    task_string = task_string.split('\n')[1:-2][0]
    embedding2 = embedding_model.encode(task_string)
    assert np.all(embedding1 == embedding2)


def test_make_embeddings_mapping():
    """Tests make_embeddings_mapping()."""
    utils.reset_flags({"llm_model_name": "davinci-002"})
    approach: LLMOpenLoopApproach = create_approach('llm-standard')
    embeddings = [[0.5], [0.1], [0.2]]
    tasks = [utils.get_custom_task('dressed', i) for i in range(1, 4)]
    dataset = [Datum(task, ['insert plan here']) for task in tasks]
    mapping = approach.make_embeddings_mapping(embeddings, dataset)
    assert len(mapping) == 3
    assert mapping[0]['embedding'] == [0.5]
    assert mapping[1]['embedding'] == [0.1]
    assert mapping[0]['datum'].solution == ['insert plan here']


def test_get_closest_datums():
    """Tests for get_closest_datums()."""
    utils.reset_flags({
        "llm_prompt_flatten_pddl": True,
        "embedding_model_name": "paraphrase-MiniLM-L6-v2",
        "llm_model_name": "davinci-002",
        "llm_prompt_method": "standard"
    })
    approach: LLMOpenLoopApproach = create_approach('llm-standard')
    dressed01 = utils.get_custom_task('dressed', 1)
    tasks = [utils.get_custom_task('dressed', i) for i in range(2, 5)]
    blocks01 = utils.get_pyperplan_benchmark_task('blocks', 1)
    blocks02 = utils.get_pyperplan_benchmark_task('blocks', 2)
    depot01 = utils.get_pyperplan_benchmark_task('depot', 1)
    tasks.append(blocks01)
    embedding_model = SentenceTransformer("paraphrase-MiniLM-L6-v2")
    embeddings = [approach.embed_task(task, embedding_model) for task in tasks]
    dataset = [Datum(task, ['insert plan here']) for task in tasks]
    embeddings_mapping = approach.make_embeddings_mapping(embeddings, dataset)
    # checking correct output size
    most_similar = approach.get_closest_datums(dressed01, embeddings_mapping,
                                               1)
    assert len(most_similar) == 1
    most_similar2 = approach.get_closest_datums(dressed01, embeddings_mapping,
                                                3)
    assert len(most_similar2) == 3
    most_similar3 = approach.get_closest_datums(dressed01, embeddings_mapping,
                                                4)
    assert len(most_similar3) == 4
    # checking that blocks is the least likely:
    assert most_similar3[0].task == utils.get_pyperplan_benchmark_task(
        'blocks', 1)
    dif_tasks = [dressed01, blocks01, depot01]
    dif_embeddings = [
        approach.embed_task(task, embedding_model) for task in dif_tasks
    ]
    dif_dataset = [Datum(task, ['insert plan here']) for task in dif_tasks]
    dif_emb_map = approach.make_embeddings_mapping(dif_embeddings, dif_dataset)
    most_sim1 = approach.get_closest_datums(blocks02, dif_emb_map, 1)
    # checking that blocks is the most likely of the 3:
    assert most_sim1[0].task == utils.get_pyperplan_benchmark_task('blocks', 1)
    # big example selecting the correct tasks each time:
    dressed = [utils.get_custom_task('dressed', i) for i in range(2, 5)]
    depot = [
        utils.get_pyperplan_benchmark_task('depot', i) for i in range(2, 5)
    ]
    blocks = [
        utils.get_pyperplan_benchmark_task('blocks', i) for i in range(2, 5)
    ]
    big_tasks = dressed + depot + blocks
    big_embeddings = [
        approach.embed_task(task, embedding_model) for task in big_tasks
    ]
    big_dataset = [Datum(task, ['insert plan here']) for task in big_tasks]
    big_emb_map = approach.make_embeddings_mapping(big_embeddings, big_dataset)
    # comparing to dressed:
    most_similar_dressed = approach.get_closest_datums(dressed01, big_emb_map,
                                                       9)
    assert len(most_similar_dressed) == len(big_tasks)
    for datum in most_similar_dressed[-3:]:
        assert datum.task in dressed

    # comparing to blocks:
    most_similar_blocks = approach.get_closest_datums(blocks01, big_emb_map, 9)
    for datum in most_similar_blocks[-3:]:
        assert datum.task in blocks

    # comparing to depot:
    most_similar_depot = approach.get_closest_datums(depot01, big_emb_map, 9)
    for datum in most_similar_depot[-3:]:
        assert datum.task in depot

    # proving identical is considered best:
    most_sim = approach.get_closest_datums(blocks02, big_emb_map, 9)[-1]
    assert most_sim.task == utils.get_pyperplan_benchmark_task('blocks', 2)
    # example to compare within a specific domain.
    dif_blocks_tasks = [
        utils.get_pyperplan_benchmark_task('blocks', 3),
        utils.get_pyperplan_benchmark_task('blocks', 35)
    ]
    dif_blocks_embeddings = [
        approach.embed_task(task, embedding_model) for task in dif_blocks_tasks
    ]
    dif_blocks_dataset = [
        Datum(task, ['insert plan here']) for task in dif_blocks_tasks
    ]
    dif_blocks_emb_map = approach.make_embeddings_mapping(
        dif_blocks_embeddings, dif_blocks_dataset)
    # Comparing blocks03 and blocks35 in their similarity to blocks01.
    # Heuristically, blocks03 should be considered more similar.
    most_sim_blocks_datum = approach.get_closest_datums(
        blocks01, dif_blocks_emb_map, 1)[0]
    assert most_sim_blocks_datum.task == utils.get_pyperplan_benchmark_task(
        'blocks', 3)


def test_get_cosine_sim():
    """Tests get_cosine_sim()."""
    utils.reset_flags({"llm_model_name": "davinci-002"})
    approach: LLMOpenLoopApproach = create_approach('llm-standard')
    embedding_model = SentenceTransformer("paraphrase-MiniLM-L6-v2")
    embedding1 = embedding_model.encode('hello')
    embedding2 = embedding_model.encode('hello')
    cos_sim1 = approach.get_cosine_sim(embedding1, embedding2)
    # cos_sim1 should be 1.
    assert abs(cos_sim1 - 1) < 0.00001
    embedding3 = embedding_model.encode('hell')
    cos_sim2 = approach.get_cosine_sim(embedding1, embedding3)
    # cos_sim2 should not be 1.
    assert cos_sim2 != 1
    embedding4 = embedding_model.encode('my name is')
    embedding5 = embedding_model.encode('my dog is here')
    cos_sim3 = approach.get_cosine_sim(embedding4, embedding5)
    assert cos_sim3 == cos_sim(embedding4, embedding5).item()
