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

    Max numbers are exclusive, so if you want exactly two people set min
    to 2 and max to 3.
    """
    problems = []
    for _ in range(num_probs):
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
    """Generates a single problem with the given parameters."""
    assert num_people >= (num_casual_events + num_formal_in_dress +
                          num_formal_in_suit)
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
    # making initial ground atoms:
    init_preds = ''
    for person in persons:
        init_preds += (f'(wearing-nothing-formal {person})\n         ' +
                       f'(wearing-nothing-casual {person})\n         ')
    for clothing in (dresses + sweatpants + sweatshirts + nicepants +
                     collaredshirt + suitjacket):
        init_preds += f'(in-closet {clothing})' + '\n         '
    # making goal ground atoms:
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


if __name__ == "__main__":  # pragma: no cover
    import os
    loc = os.path.dirname(os.path.realpath(__file__))

    # 2 levels of difficulty:
    rng_default = np.random.default_rng(seed=0)
    generated_tasks: List[str] = []
    # level one:
    generated_tasks += _generate_dressing_problems(min_people=4,
                                                   max_people=8,
                                                   min_casual=1,
                                                   max_casual=3,
                                                   min_formal_dress=1,
                                                   max_formal_dress=3,
                                                   min_formal_suit=1,
                                                   max_formal_suit=3,
                                                   min_extra_clothes=0,
                                                   max_extra_clothes=3,
                                                   num_probs=5,
                                                   rng=rng_default)
    # level two:
    generated_tasks += _generate_dressing_problems(min_people=10,
                                                   max_people=17,
                                                   min_casual=4,
                                                   max_casual=8,
                                                   min_formal_dress=3,
                                                   max_formal_dress=6,
                                                   min_formal_suit=3,
                                                   max_formal_suit=6,
                                                   min_extra_clothes=2,
                                                   max_extra_clothes=6,
                                                   num_probs=25,
                                                   rng=rng_default)
    assert len(generated_tasks) == 30

    # writing the 30 questions:
    loc = os.path.dirname(os.path.realpath(__file__))
    for q_num, q in enumerate(generated_tasks):
        q_num += 1
        file_path = loc + f'/task{str(q_num).zfill(2)}.pddl'
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(q)
