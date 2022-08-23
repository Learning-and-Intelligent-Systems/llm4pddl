"""Main script for running experiments."""

import logging
import os
import pickle
import sys
import time
from pathlib import Path

import numpy as np

from llm4pddl import utils
from llm4pddl.approaches import create_approach
from llm4pddl.approaches.base_approach import BaseApproach
from llm4pddl.dataset import create_dataset
from llm4pddl.envs import create_env
from llm4pddl.envs.base_env import BaseEnv
from llm4pddl.flags import FLAGS, parse_flags
from llm4pddl.structs import Metrics, TaskMetrics


def _main() -> None:
    """The main entry point."""
    script_start = time.time()
    str_args = " ".join(sys.argv)
    # Parse command-line flags.
    parse_flags()
    # Set up logging.
    logging.basicConfig(level=FLAGS.loglevel,
                        format="%(message)s",
                        handlers=[logging.StreamHandler()])
    logging.info(f"Running command: python {str_args}")
    logging.info("Full config:")
    logging.info(FLAGS)
    logging.info(f"Git commit hash: {utils.get_git_commit_hash()}")
    # Create the approach and env.
    # The approach is seeded in BaseApproach.__init__() using FLAGS.seed.
    approach = create_approach(FLAGS.approach)
    env = create_env(FLAGS.env)
    # Run the pipeline.
    _run_pipeline(approach, env)
    script_time = time.time() - script_start
    logging.info(f"\n\nMain script terminated in {script_time:.5f} seconds")


def _run_pipeline(approach: BaseApproach, env: BaseEnv) -> None:
    """Run training and evaluation."""
    # Run training for learning-based approaches.
    if approach.is_learning_based:
        train_tasks = env.get_train_tasks()  #list of tasks
        dataset = create_dataset(train_tasks)
        approach.train(dataset)
        # Embedding the training tasks.
        if FLAGS.use_dynamic_examples:
            embeddings = utils.embed_training_tasks(train_tasks)
            approach.embeddings_mapping = utils.make_embeddings_mapping(
                embeddings, dataset)
    # Run evaluation for all approaches.
    eval_tasks = env.get_eval_tasks()
    results = _run_evaluation(approach, eval_tasks, env.get_name())
    # Save the results.
    os.makedirs(FLAGS.results_dir, exist_ok=True)
    outdata = {
        "config": FLAGS,
        "results": results.copy(),
        "git_commit_hash": utils.get_git_commit_hash()
    }
    outfile = Path(FLAGS.results_dir) / f"{utils.get_config_path_str()}.pkl"
    with open(outfile, "wb") as f:
        pickle.dump(outdata, f)


def _run_evaluation(approach, eval_tasks, env_name) -> Metrics:
    """Evaluate the approach in the evaluation tasks."""
    results: Metrics = {}
    num_eval_tasks = len(eval_tasks)
    num_solved = 0
    for i, task in enumerate(eval_tasks):
        # Save metrics for this task.
        task_metrics: TaskMetrics = {}
        task_id = f"{env_name}__{task.problem_file.stem}"
        results[task_id] = task_metrics
        # Get a plan.
        start_time = time.time()
        plan, solve_metrics = approach.solve(task)
        solve_time = time.time() - start_time
        task_metrics["solve_time"] = solve_time
        if approach.is_planning_based:
            task_metrics["nodes_created"] = solve_metrics["nodes_created"]
            task_metrics["nodes_expanded"] = solve_metrics["nodes_expanded"]
        else:
            task_metrics["nodes_created"] = np.nan
            task_metrics["nodes_expanded"] = np.nan
        # If the approach didn't find any plan, this is a failure.
        if plan is None:
            logging.info(f"Task {i+1} / {num_eval_tasks}: "
                         f"Approach failed to find any plan.")
            task_metrics["result"] = "no_plan_found"
            continue
        # Validate the plan.
        is_valid = utils.validate_plan(task, plan)
        if not is_valid:
            logging.info(f"Task {i+1} / {num_eval_tasks}: "
                         f"Approach returned an invalid plan.")
            task_metrics["result"] = "invalid_plan"
        # Found a good plan!
        else:
            logging.info(f"Task {i+1} / {num_eval_tasks}: SOLVED")
            task_metrics["result"] = "success"
            num_solved += 1
    logging.info(f"FINAL RESULT: {num_solved} / {num_eval_tasks} solved.")
    return results


if __name__ == "__main__":  # pragma: no cover
    _main()
