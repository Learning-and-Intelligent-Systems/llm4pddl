"""Tests for RandomActionsApproach()."""

import tempfile

from llm4pddl import utils
from llm4pddl.approaches.random_actions_approach import RandomActionsApproach
from llm4pddl.structs import Task


def test_random_actions_approach():
    """Tests for RandomActionsApproach()."""
    utils.reset_flags({
        "random_actions_max_steps": 2,
        "planning_timeout": 1000
    })
    approach = RandomActionsApproach()
    assert not approach.is_learning_based
    assert not approach.is_planning_based
    # Create a trivial two-step task where there is only one action applicable
    # at each step. The random approach should solve it.
    domain_str = """(define (domain two-step)
  (:predicates (state1) (state2) (state3) (state4))

  (:action action1
        :parameters ()
        :precondition (state1)
        :effect (and (not (state1)) (state2))
  )

  (:action action2
        :parameters ()
        :precondition (state2)
        :effect (and (not (state2)) (state3))
  ))"""

    domain_file = tempfile.NamedTemporaryFile(delete=False,
                                              suffix=".pddl").name
    with open(domain_file, "w", encoding="utf-8") as f:
        f.write(domain_str)

    problem_str1 = """(define (problem two-step-problem1)
    (:domain two-step)
    (:objects )
    (:init (state1))
    (:goal (state3))
    )"""

    problem_file1 = tempfile.NamedTemporaryFile(delete=False,
                                                suffix=".pddl").name
    with open(problem_file1, "w", encoding="utf-8") as f:
        f.write(problem_str1)

    task1 = Task(domain_file, problem_file1)

    plan, _ = approach.solve(task1)
    assert utils.validate_plan(task1, plan)

    # Test timeout.
    utils.reset_flags({
        "random_actions_max_steps": 1000,
        "planning_timeout": 0.0
    })
    plan, _ = approach.solve(task1)
    assert len(plan) == 0
    assert not utils.validate_plan(task1, plan)

    # Test that no plan is found when there's a dead-end.
    problem_str2 = """(define (problem two-step-problem2)
    (:domain two-step)
    (:objects )
    (:init (state1))
    (:goal (state4))
    )"""

    problem_file2 = tempfile.NamedTemporaryFile(delete=False,
                                                suffix=".pddl").name
    with open(problem_file2, "w", encoding="utf-8") as f:
        f.write(problem_str2)

    task2 = Task(domain_file, problem_file2)

    plan, _ = approach.solve(task2)
    assert len(plan) == 0  # no valid operators because of filtering
    assert not utils.validate_plan(task2, plan)
