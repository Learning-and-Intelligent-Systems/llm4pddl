"""Training dataset creation."""

import logging
import os
import pickle
from pathlib import Path
from typing import Sequence

from llm4pddl import utils
from llm4pddl.flags import FLAGS
from llm4pddl.structs import Dataset, Datum, Task


def create_dataset(train_tasks: Sequence[Task],
                   attempt_loading: bool = False) -> Dataset:
    """Run planning on the train tasks to create training data."""
    dataset: Dataset = []
    # Make the cache dir.
    os.makedirs(FLAGS.data_dir, exist_ok=True)
    for task in train_tasks:
        # Cache per task.
        cache_file = Path(FLAGS.data_dir) / f"{task.task_id}.data"
        if attempt_loading and os.path.exists(cache_file):
            with open(cache_file, "rb") as f:
                solution = pickle.load(f)
            logging.debug(f"Loaded solution from {cache_file}")
        else:
            solution, _ = utils.run_planning(task,
                                             planner=FLAGS.data_gen_planner)
            assert solution is not None
            with open(cache_file, "wb") as f:
                pickle.dump(solution, f)
            logging.debug(f"Saved solution to {cache_file}")
        datum = Datum(task, solution)
        dataset.append(datum)
    return dataset
