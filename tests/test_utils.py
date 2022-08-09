"""Tests for utils.py."""

import os
import tempfile

import numpy as np
import pytest

from llm4pddl import utils
from llm4pddl.structs import Task


@pytest.fixture(scope="module", name="domain_file")
def _create_domain_file():
    domain_str = """;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;;; 4 Op-blocks world
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

(define (domain BLOCKS)
  (:requirements :strips :typing)
  (:types block)
  (:predicates (on ?x - block ?y - block)
	       (ontable ?x - block)
	       (clear ?x - block)
	       (handempty)
	       (holding ?x - block)
	       )

  (:action pick-up
	     :parameters (?x - block)
	     :precondition (and (clear ?x) (ontable ?x) (handempty))
	     :effect
	     (and (not (ontable ?x))
		   (not (clear ?x))
		   (not (handempty))
		   (holding ?x)))

  (:action put-down
	     :parameters (?x - block)
	     :precondition (holding ?x)
	     :effect
	     (and (not (holding ?x))
		   (clear ?x)
		   (handempty)
		   (ontable ?x)))
  (:action stack
	     :parameters (?x - block ?y - block)
	     :precondition (and (holding ?x) (clear ?y))
	     :effect
	     (and (not (holding ?x))
		   (not (clear ?y))
		   (clear ?x)
		   (handempty)
		   (on ?x ?y)))
  (:action unstack
	     :parameters (?x - block ?y - block)
	     :precondition (and (on ?x ?y) (clear ?x) (handempty))
	     :effect
	     (and (holding ?x)
		   (clear ?y)
		   (not (clear ?x))
		   (not (handempty))
		   (not (on ?x ?y)))))
"""
    domain_file = tempfile.NamedTemporaryFile(delete=False,
                                              suffix=".pddl").name
    with open(domain_file, "w", encoding="utf-8") as f:
        f.write(domain_str)
    return domain_file


@pytest.fixture(scope="module", name="problem_file")
def _create_problem_file():
    problem_str = """(define (problem blocks)
    (:domain blocks)
    (:objects
        d - block
        b - block
        a - block
        c - block
    )
    (:init
        (clear c)
        (clear b)
        (clear d)
        (ontable c)
        (ontable a)
        (ontable d)
        (on b a)
        (handempty)
    )
    (:goal (and (holding a)))
)
"""
    problem_file = tempfile.NamedTemporaryFile(delete=False,
                                               suffix=".pddl").name
    with open(problem_file, "w", encoding="utf-8") as f:
        f.write(problem_str)
    return problem_file


@pytest.fixture(scope="module", name="impossible_problem_file")
def _create_impossible_problem_file():
    problem_str = """(define (problem blocks)
    (:domain blocks)
    (:objects
        d - block
        b - block
        a - block
        c - block
    )
    (:init
        (clear c)
        (clear b)
        (clear d)
        (ontable c)
        (ontable d)
        (handempty)
    )
    (:goal (and (holding a)))
)
"""
    problem_file = tempfile.NamedTemporaryFile(delete=False,
                                               suffix=".pddl").name
    with open(problem_file, "w", encoding="utf-8") as f:
        f.write(problem_str)
    return problem_file


@pytest.fixture(scope="module", name="valid_plans")
def _create_valid_plans():
    # Optimal valid plan.
    valid_plan1 = ["(unstack b a)", "(stack b c)", "(pick-up a)"]
    # Not optimal, but still valid.
    valid_plan2 = [
        "(unstack b a)", "(stack b c)", "(unstack b c)", "(stack b c)",
        "(pick-up a)"
    ]
    valid_plans = [valid_plan1, valid_plan2]
    return valid_plans


@pytest.fixture(scope="module", name="invalid_plans")
def _create_invalid_plans():
    # Invalid because the second action's preconditions do not hold.
    invalid_plan1 = [
        "(unstack b a)", "(unstack b a)", "(stack b c)", "(pick-up a)"
    ]
    # Invalid because there's a garbage entry.
    invalid_plan2 = ["garbage", "(unstack b a)", "(stack b c)", "(pick-up a)"]
    # Invalid because the plan stops short.
    invalid_plan3 = [
        "(unstack b a)",
        "(stack b c)",
    ]
    invalid_plans = [invalid_plan1, invalid_plan2, invalid_plan3]
    return invalid_plans


def test_validate_plan(domain_file, problem_file, valid_plans, invalid_plans):
    """Tests for validate_plan()."""
    task = Task(domain_file, problem_file)
    for valid_plan in valid_plans:
        assert utils.validate_plan(task, valid_plan)
    for invalid_plan in invalid_plans:
        assert not utils.validate_plan(task, invalid_plan)


def test_get_pyperplan_benchmark_task():
    """Tests for get_pyperplan_benchmark_task()."""
    # Standard domain format.
    task = utils.get_pyperplan_benchmark_task("blocks", 1)
    assert os.path.exists(task.domain_file)
    assert os.path.exists(task.problem_file)
    # Per-problem domain files.
    task = utils.get_pyperplan_benchmark_task("airport", 1)
    assert os.path.exists(task.domain_file)
    assert os.path.exists(task.problem_file)
    # Domain doesn't exist.
    with pytest.raises(FileNotFoundError) as e:
        utils.get_pyperplan_benchmark_task("not a real domain", 1)
    assert "Domain not found" in str(e)
    # Problem doesn't exist.
    with pytest.raises(FileNotFoundError) as e:
        utils.get_pyperplan_benchmark_task("blocks", 100)
    assert "Problem not found" in str(e)


def test_get_custom_task():
    """Tests get_custom_task()"""
    # Dressed:
    task = utils.get_custom_task("dressed", 1)
    assert os.path.exists(task.domain_file)
    assert os.path.exists(task.problem_file)
    # Domain doesn't exist:
    with pytest.raises(FileNotFoundError) as f:
        task = utils.get_custom_task("nonsense", 1)
    assert "Domain not found" in str(f)
    # Problem doesn't exist:
    with pytest.raises(FileNotFoundError) as f:
        task = utils.get_custom_task("dressed", 100)
    assert "Task not found" in str(f)


def test_run_planning(domain_file, problem_file, impossible_problem_file):
    """Tests for run_planning().

    Fast downward is not tested because it's not easy to install on the
    github checks server.
    """
    utils.reset_flags({"planner": "pyperplan", "planning_timeout": 100})
    # Test planning successfully.
    rng = np.random.default_rng(123)
    task = Task(domain_file, problem_file)
    plan, metrics = utils.run_planning(task, rng)
    assert metrics["nodes_created"] > metrics["nodes_expanded"]
    assert plan is not None
    assert utils.validate_plan(task, plan)
    # Test planning in an impossible problem.
    impossible_task = Task(domain_file, impossible_problem_file)
    plan, metrics = utils.run_planning(impossible_task, rng)
    assert metrics["nodes_created"] == metrics["nodes_expanded"] == 1
    assert plan is None
    # Test planning in a pyperplan benchmark problem.
    task = utils.get_pyperplan_benchmark_task("blocks", 1)
    plan, metrics = utils.run_planning(task, rng)
    assert metrics["nodes_created"] > metrics["nodes_expanded"]
    assert plan is not None
    assert utils.validate_plan(task, plan)
    # Test planning with an invalid planner.
    utils.reset_flags({"planner": "not a real planner"})
    with pytest.raises(NotImplementedError) as e:
        utils.run_planning(task, rng)
    assert "Unrecognized planner" in str(e)
