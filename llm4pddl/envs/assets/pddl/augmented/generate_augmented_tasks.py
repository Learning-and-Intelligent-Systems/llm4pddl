"""Data augmentation script.

Usage example:

    python llm4pddl/envs/assets/pddl/augmented/generate_augmented_tasks.py
"""

import abc
import argparse
import heapq
import os
import tempfile
from pathlib import Path
from typing import Iterator, List, Sequence

from llm4pddl import utils
from llm4pddl.envs import PYPERPLAN_BENCHMARKS
from llm4pddl.flags import FLAGS
from llm4pddl.structs import PyperplanProblem, Task


def _problem_to_task(problem: PyperplanProblem, domain_file: Path) -> Task:
    problem_str = utils.pyperplan_problem_to_str(problem)
    problem_file = tempfile.NamedTemporaryFile(delete=False,
                                               suffix=".pddl").name
    with open(problem_file, "w", encoding="utf-8") as f:
        f.write(problem_str)
    return Task(domain_file, Path(problem_file))


class _DataAugmentationSearchOperator(abc.ABC):
    """Helper for augment_tasks()."""

    def get_successors(self, task: Task) -> Iterator[Task]:
        """Generate successor tasks."""
        _, problem = utils.parse_task(task)
        for new_problem in self._get_successor_problems(problem):
            new_task = _problem_to_task(new_problem, task.domain_file)
            # Check if plan is trivial or not found.
            plan, _ = utils.run_planning(new_task, FLAGS.data_gen_planner)
            if not plan:
                os.remove(new_task.problem_file)
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


def _greedy_minimize(task: Task) -> Task:
    print(f"Greedily minimizing task {task.task_id}")
    domain_file = task.domain_file
    # Greedily remove initial state atoms.
    _, problem = utils.parse_task(task)
    for init_to_remove in list(problem.initial_state):
        new_initial_state = [
            a for a in problem.initial_state if a != init_to_remove
        ]
        assert len(new_initial_state) < len(problem.initial_state)
        new_problem = PyperplanProblem(problem.name, problem.domain,
                                       problem.objects, new_initial_state,
                                       problem.goal)
        new_task = _problem_to_task(new_problem, domain_file)
        # Check if plan is trivial or not found.
        plan, _ = utils.run_planning(new_task, FLAGS.data_gen_planner)
        if not plan:
            os.remove(new_task.problem_file)
            continue
        # Update the problem.
        problem = new_problem
    # Greedily remove objects. We could only ever remove objects that are
    # in neither the initial state nor the goal.
    used_objects = {
        o
        for a in problem.initial_state + problem.goal for o, _ in a.signature
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
        new_task = _problem_to_task(new_problem, domain_file)
        # Check if plan is trivial or not found.
        plan, _ = utils.run_planning(new_task, FLAGS.data_gen_planner)
        if not plan:
            os.remove(new_task.problem_file)
            continue
        # Update the problem.
        problem = new_problem
    # Create the final task.
    return _problem_to_task(problem, domain_file)


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

    remove_goal_gen = _DataAugmentationGoalRemovalOperator()

    # Greedy search with respect to task size.
    queue = [(utils.get_task_size(t), i, t)
             for i, t in enumerate(original_tasks)]
    tiebreak = len(original_tasks)
    visited = {t.problem_str for t in original_tasks}

    # Start by minimizing the original tasks.
    for task in original_tasks:
        succ = _greedy_minimize(task)
        if succ.problem_str not in visited:
            visited.add(succ.problem_str)
            tiebreak += 1
            new_tasks.append(succ)
            succ_prio = utils.get_task_size(succ)
            heapq.heappush(queue, (succ_prio, tiebreak, succ))

    for it in range(num_iters):
        if not queue:
            print("Data augmentation queue exhausted.")
            break
        print(f"Data augmentation iteration {it}/{num_iters}")
        _, _, task = heapq.heappop(queue)
        print(f"Popped task with size: {utils.get_task_size(task)}")
        for succ in remove_goal_gen.get_successors(task):
            print(f"Task size before minimize: {utils.get_task_size(succ)}")
            succ = _greedy_minimize(succ)
            print(f"Task size after minimize: {utils.get_task_size(succ)}")
            if succ.problem_str in visited:
                continue
            visited.add(succ.problem_str)
            tiebreak += 1
            new_tasks.append(succ)
            succ_prio = utils.get_task_size(succ)
            heapq.heappush(queue, (succ_prio, tiebreak, succ))

    print(f"Data augmentation generated {len(new_tasks)} tasks "
          f"(including the original {len(original_tasks)} tasks).")

    return new_tasks


def _save_tasks(tasks: Sequence[Task], save_path: Path) -> None:
    assert len(tasks) > 0
    os.makedirs(save_path, exist_ok=True)
    # Check whether to save one or several domain files.
    if tasks[0].domain_file.name == "domain.pddl":
        assert all(t.domain_file.name == "domain.pddl" for t in tasks)
        with open(save_path / "domain.pddl", "w", encoding="utf-8") as f:
            f.write(tasks[0].domain_str)
    else:
        for i, task in enumerate(tasks):
            domain_file_path = save_path / f"domain{i+1}.pddl"
            with open(domain_file_path, "w", encoding="utf-8") as f:
                f.write(task.domain_str)
    # Save the problem files.
    for i, task in enumerate(tasks):
        problem_file_path = save_path / f"task{i+1}.pddl"
        with open(problem_file_path, "w", encoding="utf-8") as f:
            f.write(task.problem_str)
    print(f"Saved tasks to {save_path}")


def _generate_tasks_for_env(original_task_dir: Path, out_dir: Path,
                            num_original_train_tasks: int,
                            max_num_iters: int) -> None:
    # Load all the original tasks.
    all_tasks = utils.get_all_tasks_from_dir(original_task_dir)
    assert len(all_tasks) >= num_original_train_tasks
    # Split into train and eval.
    train_tasks = all_tasks[:num_original_train_tasks]
    eval_tasks = all_tasks[num_original_train_tasks:]
    # Augment the train tasks.
    new_train_tasks = _augment_tasks(train_tasks, max_num_iters)
    # Make the outdirs.
    out_path = Path(out_dir)
    train_path = out_path / "train"
    eval_path = out_path / "eval"
    _save_tasks(new_train_tasks, train_path)
    _save_tasks(eval_tasks, eval_path)


def _main(num_original_train_tasks: int, max_num_iters: int) -> None:
    for benchmark_name in PYPERPLAN_BENCHMARKS:
        print(f"******** Starting augmentation for {benchmark_name} *********")
        original_task_dir = utils.PYPERPLAN_BENCHMARK_DIR / benchmark_name
        out_dir = utils.AUGMENTED_BENCHMARK_DIR / f"pyperplan-{benchmark_name}"
        _generate_tasks_for_env(original_task_dir, out_dir,
                                num_original_train_tasks, max_num_iters)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--num_original_train_tasks", default=5, type=int)
    parser.add_argument("--max_num_iters", default=100, type=int)
    parser.add_argument("--data_gen_planner", default="fastdownward", type=str)
    parser.add_argument("--planning_timeout", default=100.0, type=float)
    args = parser.parse_args()
    utils.reset_flags({
        "data_gen_planner": args.data_gen_planner,
        "planning_timeout": args.planning_timeout,
    })
    _main(args.num_original_train_tasks, args.max_num_iters)
