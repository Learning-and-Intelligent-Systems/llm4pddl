"""Generates dressed pddl problems."""

from typing import List

import numpy as np


def _generate_dressing_problems(min_people: int, max_people: int,
                                min_casual: int, max_casual: int,
                                min_formal_dress: int, max_formal_dress: int,
                                min_formal_suit: int, max_formal_suit: int,
                                min_extra_clothes: int, max_extra_clothes: int,
                                num_probs: int,
                                rng: np.random.Generator) -> List[str]:
    """Generates problems from a distribution.

    max numbers are exclusive, so if you want exactly two people set min
    to 2 and max to 3.
    """
    problems = []
    for _ in range(1, num_probs + 1):
        num_people = rng.integers(min_people, max_people)
        num_casual = rng.integers(min_casual, max_casual)
        num_formal_dress = rng.integers(min_formal_dress, max_formal_dress)
        num_formal_suit = rng.integers(min_formal_suit, max_formal_suit)
        num_extra = rng.integers(min_extra_clothes, max_extra_clothes)
        if num_people < num_casual + num_formal_dress + num_formal_suit:
            num_people = num_casual + num_formal_dress + num_formal_suit

        problem = _generate_dressing_problem(num_people, num_casual,
                                             num_formal_dress, num_formal_suit,
                                             num_extra, rng)
        problems.append(problem)
    return problems


def _generate_dressing_problem(num_people: int, num_casual_events: int,
                               num_formal_in_dress: int,
                               num_formal_in_suit: int, num_extra_objects: int,
                               rng: np.random.Generator) -> str:
    assert num_people >= num_casual_events + num_formal_in_dress + num_formal_in_suit
    # deciding extra clothing:
    extras = ['ex_p', 'ex_d', 'ex_sp', 'ex_ss', 'ex_np', 'ex_cs', 'ex_sj']
    exs = {ex: 0 for ex in extras}
    for _ in range(num_extra_objects):
        exs[rng.choice(extras)] += 1
    # making objects:
    persons = [f'person{i}' for i in range(1, num_people + 1 + exs['ex_p'])]
    dresses = [
        f'dress{i}' for i in range(1, num_formal_in_dress + 1 + exs['ex_d'])
    ]
    sweatpants = [
        f'sweatpants{i}'
        for i in range(1, num_casual_events + 1 + exs['ex_sp'])
    ]
    sweatshirts = [
        f'sweatshirt{i}'
        for i in range(1, num_casual_events + 1 + exs['ex_ss'])
    ]
    nicepants = [
        f'nice-pants{i}'
        for i in range(1, num_formal_in_suit + 1 + exs['ex_np'])
    ]
    collaredshirt = [
        f'collared-shirt{i}'
        for i in range(1, num_formal_in_suit + 1 + exs['ex_cs'])
    ]
    suitjacket = [
        f'suit-jacket{i}'
        for i in range(1, num_formal_in_suit + 1 + exs['ex_d'])
    ]
    objects = [{
        'type': 'person',
        'objs': persons
    }, {
        'type': 'dress',
        'objs': dresses
    }, {
        'type': 'sweatpants',
        'objs': sweatpants
    }, {
        'type': 'sweatshirt',
        'objs': sweatshirts
    }, {
        'type': 'nice-pants',
        'objs': nicepants
    }, {
        'type': 'collared-shirt',
        'objs': collaredshirt
    }, {
        'type': 'suit-jacket',
        'objs': suitjacket
    }]
    object_str = ''
    for obj in objects:
        if len(obj['objs']) > 0:
            object_str += ' '.join(
                obj['objs']) + f' - {obj["type"]}\n            '
    # making initial predicates:
    init_preds = ''
    for person in persons:
        init_preds += (f'(wearing-nothing-formal {person})\n         ' +
                       f'(wearing-nothing-casual {person})\n         ')
    for clothing in (dresses + sweatpants + sweatshirts + nicepants +
                     collaredshirt + suitjacket):
        init_preds += f'(in-closet {clothing})' + '\n         '
    # making goal predicates:
    goals = ''
    goal_predicates = []
    rng.shuffle(persons)
    for i in range(num_casual_events):
        goal_predicates.append(
            f'(attending-casual-event {persons[i]})\n              ')
    for i in range(
            num_casual_events,
        (num_casual_events + num_formal_in_dress + num_formal_in_suit)):
        goal_predicates.append(
            f'(attending-formal-event {persons[i]})\n              ')
    rng.shuffle(goal_predicates)
    for goal in goal_predicates:
        goals += goal
    #making problem:
    problem_string = f"""(define (problem dressed)
  (:domain dressed)
  (:objects {object_str})
  (:init {init_preds})
  (:goal (and {goals}))
  )"""
    return problem_string


def test_generate_dressing_problems() -> None:
    rng = np.random.default_rng(seed=0)
    prob1 = _generate_dressing_problems(2, 3, 2, 3, 0, 1, 0, 1, 0, 1, 1,
                                        rng)[0]
    rng2 = np.random.default_rng(seed=0)
    reference_prob = _generate_dressing_problem(2, 2, 0, 0, 0, rng2)
    assert prob1 == reference_prob


def test_generate_dressing_problem() -> None:
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


if __name__ == "__main__":
    import os
    loc = os.path.dirname(os.path.realpath(__file__))
    test_generate_dressing_problem()
    test_generate_dressing_problems()

    # 4 levels of difficulty:
    rng = np.random.default_rng(seed=0)
    thirty: List[str] = []
    # TODO
    # level one:
    thirty += _generate_dressing_problems(4, 5, 0, 3, 0, 2, 0, 2, 0, 2, 7, rng)
    # level two:
    thirty += _generate_dressing_problems(4, 7, 2, 4, 1, 3, 1, 3, 0, 2, 7, rng)
    # level three:
    thirty += _generate_dressing_problems(7, 11, 3, 6, 2, 4, 2, 4, 1, 4, 8,
                                          rng)
    # level four:
    thirty += _generate_dressing_problems(10, 14, 4, 7, 3, 5, 3, 5, 2, 5, 8,
                                          rng)
    assert len(thirty) == 30

    # writing the 30 questions:
    loc = os.path.dirname(os.path.realpath(__file__))
    for i, q in enumerate(thirty):
        i += 1
        file_path = loc + f'/task{str(i).zfill(2)}.pddl'
        if not os.path.exists(file_path):
            with open(file_path, 'w') as f:
                f.write(q)
