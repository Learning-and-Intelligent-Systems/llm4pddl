import numpy as np

from llm4pddl.envs.assets.pddl.dressed.generate_tasks import \
    _generate_dressing_problem, _generate_dressing_problems


def test_generate_dressing_problems() -> None:
    """Tests the function _generate_dressing_problems."""
    rng = np.random.default_rng(seed=0)
    prob1 = _generate_dressing_problems(2, 3, 2, 3, 0, 1, 0, 1, 0, 1, 1,
                                        rng)[0]
    rng2 = np.random.default_rng(seed=0)
    reference_prob = _generate_dressing_problem(2, 2, 0, 0, 0, rng2)
    assert prob1 == reference_prob


def test_generate_dressing_problem() -> None:
    """Tests the function _generate_dressing_problem."""
    rng = np.random.default_rng(seed=0)
    out = _generate_dressing_problem(2, 2, 0, 0, 0, rng)
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
