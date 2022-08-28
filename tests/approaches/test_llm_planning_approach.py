"""Tests for the LLM planning approach."""

import shutil

from test_llm_open_loop_approach import _MockLLM

from llm4pddl import utils
from llm4pddl.approaches import create_approach
from llm4pddl.dataset import create_dataset
from llm4pddl.envs import create_env


def test_llm_planning_planning_approach():
    """Tests for LLMPlanningApproach()."""
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
        "llm_prompt_method": "standard",
        "llm_plan_guidance_method": "init-queue",
        "planner": "pyperplan",
        "data_gen_planner": "pyperplan",
        "data_gen_method": "planning",
        "planning_timeout": 100,
        "llm_prompt_flatten_pddl": False,
        "use_dynamic_examples": False,
        "data_dir": data_dir,
        "load_data": False
    })
    env = create_env("pyperplan-gripper")
    train_tasks = env.get_train_tasks()
    approach = create_approach("llm-standard-plan")
    assert approach.get_name() == "llm-plan"
    assert approach.is_learning_based
    assert approach.is_planning_based

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
    plan, ideal_metrics = approach.solve(task)
    assert utils.validate_plan(task, plan)
    assert ideal_metrics["nodes_expanded"] == 1

    # If the LLM response is garbage, we should still find a plan that achieves
    # the goal, because we will just fall back to regular planning.
    llm.response = "garbage"
    plan, worst_case_metrics = approach.solve(task)
    assert utils.validate_plan(task, plan)
    assert worst_case_metrics["nodes_expanded"] > 1

    # If the LLM response is suggests an invalid action, the plan should not
    # be used after that.
    llm.response = "\n".join(ideal_response.split("\n")[-1:])
    plan, worst_case_metrics2 = approach.solve(task)
    assert utils.validate_plan(task, plan)
    assert worst_case_metrics2["nodes_expanded"] == \
        worst_case_metrics["nodes_expanded"]

    # If the LLM response is almost perfect, it should be very helpful for
    # planning guidance.
    llm.response = "\n".join(ideal_response.split("\n")[:-1])
    plan, almost_ideal_metrics = approach.solve(task)
    assert utils.validate_plan(task, plan)
    worst_case_nodes = worst_case_metrics["nodes_expanded"]
    almost_ideal_nodes = almost_ideal_metrics["nodes_expanded"]
    ideal_nodes = ideal_metrics["nodes_expanded"]
    assert worst_case_nodes > almost_ideal_nodes
    assert almost_ideal_nodes > ideal_nodes

    shutil.rmtree(cache_dir)
    shutil.rmtree(data_dir)
