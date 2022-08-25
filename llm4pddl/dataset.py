"""Training dataset creation."""

import logging
import os
import pickle
from pathlib import Path
from typing import Sequence

from llm4pddl import utils
from llm4pddl.flags import FLAGS
from llm4pddl.manual_planning import create_manual_plan
from llm4pddl.structs import Dataset, Datum, Task


def create_dataset(train_tasks: Sequence[Task],
                   attempt_loading: bool = False) -> Dataset:
    """Run planning on the train tasks to create training data."""
    dataset: Dataset = []
    # Make the cache dir.
    os.makedirs(FLAGS.data_dir, exist_ok=True)
    for task in train_tasks:
        # Cache per task.
        cache_file = f"{task.task_id}__{FLAGS.data_gen_method}.data"
        cache_path = Path(FLAGS.data_dir) / cache_file
        if attempt_loading and os.path.exists(cache_path):
            with open(cache_path, "rb") as f:
                solution = pickle.load(f)
            logging.debug(f"Loaded solution from {cache_path}")
            # Sanity check the loaded solution.
            assert utils.validate_plan(task, solution)
        else:

            if FLAGS.data_gen_method == "planning":
                planner = FLAGS.data_gen_planner
                solution, _ = utils.run_planning(task, planner=planner)
                assert solution is not None

            else:
                assert FLAGS.data_gen_method == "manual"
                solution = create_manual_plan(task, FLAGS.env)

            with open(cache_path, "wb") as f:
                pickle.dump(solution, f)
            logging.debug(f"Saved solution to {cache_path}")
        datum = Datum(task, solution)
        dataset.append(datum)
    return dataset
