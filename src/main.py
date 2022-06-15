"""Main entry point for running approaches in environments."""

import logging
import time
import sys

from llm4pddl.src.args import create_arg_parser
from llm4pddl.src.approaches import create_approach
from llm4pddl.src.approaches.base_approach import BaseApproach
from llm4pddl.src.envs import create_env
from llm4pddl.src.envs.base_env import BaseEnv
from llm4pddl.src import utils
from llm4pddl.src.structs import Dataset, Metrics


def main() -> None:
    """Main entry point for running approaches in environments."""
    script_start = time.time()
    # Parse arguments.
    parser = create_arg_parser()
    parsed_args = parser.parse_args()
    # Log to stderr.
    str_args = " ".join(sys.argv)
    logging.basicConfig(level=logging.INFO,
                        format="%(message)s",
                        handlers=[logging.StreamHandler()])
    logging.info(f"Running command: python {str_args}")
    logging.info(f"Git commit hash: {utils.get_git_commit_hash()}")
    # Create classes.
    # TODO: Note that seeding happens inside the env and approach.
    env = create_env(parsed_args.env)
    approach = create_approach(parsed_args.approach, env.domain)
    if approach.is_learning_based:
        # Create training data.
        demonstrations = _generate_or_load_demos(env)
        # Allow the approach to learn.
        approach.learn_from_demonstrations(demonstrations)
    # Evaluate the approach.
    results = _run_testing(env, approach)
    # TODO: save results.
    script_time = time.time() - script_start
    logging.info(f"\n\nMain script terminated in {script_time:.5f} seconds")


def _run_testing(env: BaseEnv, approach: BaseApproach) -> Metrics:
    test_tasks = env.get_test_tasks()
    results = {
        "num_test_tasks": 0,
        "valid_solution_lengths": [],
        "num_invalid_solutions": 0,
        "num_test_tasks_solved": 0
    }
    for task in test_tasks:
        results["num_test_tasks"] += 1
        try:
            solution = approach.solve(task)
        except utils.ApproachFailure:
            continue
        # Validate the solution.
        if utils.solution_is_valid(solution, task):
            results["num_test_tasks_solved"] += 1
            results["valid_solution_lengths"].append(len(solution))
        else:
            results["num_invalid_solutions"] += 1
    return results


def _generate_or_load_demos(env: BaseEnv) -> Dataset:
    import ipdb; ipdb.set_trace()


if __name__ == "__main__":  # pragma: no cover
    main()
