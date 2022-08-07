"""Tests the generate_tasks.py file."""

import numpy as np

from llm4pddl.envs.assets.pddl.dressed.generate_tasks import \
    _generate_dressing_problem, _generate_dressing_problems


def test_generate_dressing_problems1() -> None:
    """Tests the function _generate_dressing_problems."""
    rng = np.random.default_rng(seed=0)
    prob1 = _generate_dressing_problems(min_people=2,
                                        max_people=3,
                                        min_casual=2,
                                        max_casual=3,
                                        min_formal_dress=0,
                                        max_formal_dress=1,
                                        min_formal_suit=0,
                                        max_formal_suit=1,
                                        min_extra_clothes=0,
                                        max_extra_clothes=1,
                                        num_probs=1,
                                        rng=rng)[0]
    rng2 = np.random.default_rng(seed=0)
    reference_prob = _generate_dressing_problem(num_people=2,
                                                num_casual_events=2,
                                                num_formal_in_dress=0,
                                                num_formal_in_suit=0,
                                                num_extra_objects=0,
                                                rng=rng2)
    assert prob1 == reference_prob


def test_generate_dressing_problems2() -> None:
    """Tests the function _generate_dressing_problems."""
    rng = np.random.default_rng(seed=0)
    rng2 = np.random.default_rng(seed=0)
    prob1 = _generate_dressing_problems(min_people=0,
                                        max_people=1,
                                        min_casual=1,
                                        max_casual=2,
                                        min_formal_dress=0,
                                        max_formal_dress=1,
                                        min_formal_suit=0,
                                        max_formal_suit=1,
                                        min_extra_clothes=0,
                                        max_extra_clothes=1,
                                        num_probs=1,
                                        rng=rng)[0]
    reference_prob = _generate_dressing_problem(num_people=1,
                                                num_casual_events=1,
                                                num_formal_in_dress=0,
                                                num_formal_in_suit=0,
                                                num_extra_objects=0,
                                                rng=rng2)
    assert prob1 == reference_prob


def test_generate_dressing_problem1() -> None:
    """Tests the function _generate_dressing_problem."""
    rng = np.random.default_rng(seed=0)
    out = _generate_dressing_problem(num_people=2,
                                     num_casual_events=2,
                                     num_formal_in_dress=0,
                                     num_formal_in_suit=0,
                                     num_extra_objects=0,
                                     rng=rng)
    assert out == """(define (problem dressed)
  (:domain dressed)
  (:objects person1 person2 - person
            sweatpants1 sweatpants2 - sweatpants
            sweatshirt1 sweatshirt2 - sweatshirt
            )
  (:init (wearing-nothing-formal person1)
         (wearing-nothing-casual person1)
         (wearing-nothing-formal person2)
         (wearing-nothing-casual person2)
         (in-closet sweatpants1)
         (in-closet sweatpants2)
         (in-closet sweatshirt1)
         (in-closet sweatshirt2)
         )
  (:goal (and (attending-casual-event person1)
              (attending-casual-event person2)
              ))
  )"""


def test_generate_dressing_problem2() -> None:
    """Tests the function _generate_dressing_problem."""
    rng = np.random.default_rng(seed=0)
    out = _generate_dressing_problem(num_people=1,
                                     num_casual_events=0,
                                     num_formal_in_dress=1,
                                     num_formal_in_suit=0,
                                     num_extra_objects=1,
                                     rng=rng)
    assert out == """(define (problem dressed)
  (:domain dressed)
  (:objects person1 - person
            dress1 - dress
            collared-shirt1 - collared-shirt
            )
  (:init (wearing-nothing-formal person1)
         (wearing-nothing-casual person1)
         (in-closet dress1)
         (in-closet collared-shirt1)
         )
  (:goal (and (attending-formal-event person1)
              ))
  )"""
