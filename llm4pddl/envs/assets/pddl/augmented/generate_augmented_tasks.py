"""Data augmentation script."""

import abc
import argparse
import functools
import hashlib
import heapq
import logging
import os
import re
import subprocess
import sys
import tempfile
from collections import defaultdict
from pathlib import Path
from typing import Any, Collection, Dict, Iterator, List, Optional, Sequence, \
    Set, Tuple

from llm4pddl.flags import FLAGS
from llm4pddl.structs import Plan, PyperplanAction, PyperplanDomain, \
    PyperplanPredicate, PyperplanProblem, PyperplanType, Task, TaskMetrics
from llm4pddl import utils


class _DataAugmentationSearchOperator(abc.ABC):
    """Helper for augment_tasks()."""

    def get_successors(self, task: Task) -> Iterator[Task]:
        """Generate successor tasks."""
        _, problem = utils.parse_task(task)
        for new_problem in self._get_successor_problems(problem):
            new_problem_str = utils.pyperplan_problem_to_str(new_problem)
            new_problem_file = tempfile.NamedTemporaryFile(delete=False,
                                                           suffix=".pddl").name
            with open(new_problem_file, "w", encoding="utf-8") as f:
                f.write(new_problem_str)
            new_task = Task(task.domain_file, Path(new_problem_file))
            # Check if plan is trivial or not found.
            plan, _ = utils.run_planning(new_task, FLAGS.data_gen_planner)
            if not plan:
                os.remove(new_problem_file)
                continue
            yield new_task

    @abc.abstractmethod
    def _get_successor_problems(
            self, problem: PyperplanProblem) -> Iterator[PyperplanProblem]:
        """Generate successor pyperplan problems."""
        raise NotImplementedError("Override me!")


class _DataAugmentationGoalRemovalOperator(_DataAugmentationSearchOperator):
    """Augment by removing parts of the goal."""

    def _get_successor_problems(
            self, problem: PyperplanProblem) -> Iterator[PyperplanProblem]:
        for goal_to_remove in problem.goal:
            new_goal = [g for g in problem.goal if g != goal_to_remove]
            new_problem = PyperplanProblem(problem.name, problem.domain,
                                           problem.objects,
                                           problem.initial_state, new_goal)
            yield new_problem


class _DataAugmentationInitRemovalOperator(_DataAugmentationSearchOperator):
    """Augment by removing parts of the initial state."""

    def _get_successor_problems(
            self, problem: PyperplanProblem) -> Iterator[PyperplanProblem]:
        for init_to_remove in problem.initial_state:
            new_initial_state = [
                a for a in problem.initial_state if a != init_to_remove
            ]
            assert len(new_initial_state) < len(problem.initial_state)
            new_problem = PyperplanProblem(problem.name, problem.domain,
                                           problem.objects, new_initial_state,
                                           problem.goal)
            yield new_problem


class _DataAugmentationObjectRemovalOperator(_DataAugmentationSearchOperator):
    """Augment by removing objects."""

    def _get_successor_problems(
            self, problem: PyperplanProblem) -> Iterator[PyperplanProblem]:
        # We could only ever remove objects that are in neither the initial
        # state nor the goal.
        used_objects = {
            o
            for a in problem.initial_state + problem.goal
            for o, _ in a.signature
        }
        candidate_objects = set(problem.objects) - used_objects
        for obj_to_remove in candidate_objects:
            new_objects = {
                o: problem.objects[o]
                for o in problem.objects if o != obj_to_remove
            }
            assert len(new_objects) < len(problem.objects)
            new_problem = PyperplanProblem(problem.name, problem.domain,
                                           new_objects, problem.initial_state,
                                           problem.goal)
            yield new_problem


def _augment_tasks(original_tasks: Sequence[Task],
                   num_iters: int) -> List[Task]:
    """Augment tasks to create a larger collection of smaller tasks.

    The original tasks are included in the returned tasks.

    For each original task, repeat until validation fails:
        - Greedily remove objects.
        - Greedily select a goal atom to remove.
        - Greedily remove init atoms until the problem.

    Any time the task is validated, we add it to the set of tasks.
    """
    new_tasks = list(original_tasks)

    remove_goal_gen =  _DataAugmentationGoalRemovalOperator()
    remove_obj_gen = _DataAugmentationObjectRemovalOperator()
    remove_init_gen = _DataAugmentationInitRemovalOperator()

    def _greedy_minimize(task: Task) -> Task:
        while True:
            improvement_found = False
            for gen in [remove_obj_gen, remove_init_gen]:
                for succ in gen.get_successors(task):
                    task = succ
                    improvement_found = True
                    break
            if not improvement_found:
                break
        return task

    # Greedy search with respect to task size.
    queue = [(utils.get_task_size(t), i, t) for i, t in enumerate(original_tasks)]
    tiebreak = len(original_tasks)
    visited = {t.problem_str for t in original_tasks}

    for it in range(num_iters):
        if not queue:
            logging.debug("Data augmentation queue exhausted.")
            break
        logging.debug(f"Data augmentation iteration {it}/{num_iters}")
        _, _, task = heapq.heappop(queue)
        logging.debug(f"Popped task with size: {utils.get_task_size(task)}")
        for succ in remove_goal_gen.get_successors(task):
            logging.debug(f"Task size before minimize: {utils.get_task_size(succ)}")
            succ = _greedy_minimize(succ)
            logging.debug(f"Task size after minimize: {utils.get_task_size(succ)}")
            if succ.problem_str in visited:
                continue
            visited.add(succ.problem_str)
            tiebreak += 1
            new_tasks.append(succ)
            succ_prio = utils.get_task_size(succ)
            heapq.heappush(queue, (succ_prio, tiebreak, succ))

    logging.debug(f"Data augmentation generated {len(new_tasks)} tasks "
                  f"(including the original {len(original_tasks)} tasks).")

    return new_tasks


def _main(original_task_dir: str, num_original_train_tasks: int, max_num_iters: int) -> None:
    # Load all the original tasks.
    all_tasks = utils.get_all_tasks_from_dir(Path(original_task_dir))
    assert len(original_task_dir) >= num_original_train_tasks
    # Split into train and eval.
    train_tasks = all_tasks[:num_original_train_tasks]
    eval_tasks = all_tasks[num_original_train_tasks:]
    # Augment the train tasks.
    new_tasks = _augment_tasks(train_tasks, max_num_iters)
    # Save the augmented tasks.
    import ipdb; ipdb.set_trace()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--original_task_dir", required=True, type=str)
    parser.add_argument("--num_original_train_tasks", default=5, type=int)
    parser.add_argument("--max_num_iters", default=100, type=int)
    args = parser.parse_args()
    _main(args.original_task_dir, args.num_original_train_tasks, args.max_num_iters)
