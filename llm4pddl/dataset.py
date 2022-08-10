"""Training dataset creation."""

from typing import Sequence

import numpy as np

from llm4pddl import utils
from llm4pddl.flags import FLAGS
from llm4pddl.structs import Dataset, Datum, Task


def create_dataset(train_tasks: Sequence[Task]) -> Dataset:
    """Run planning on the train tasks to create training data."""
    dataset: Dataset = []
    rng = np.random.default_rng(FLAGS.seed)
    for task in train_tasks:
        solution, _ = utils.run_planning(task,
                                         rng,
                                         planner=FLAGS.data_gen_planner)
        assert solution is not None
        datum = Datum(task, solution)
        dataset.append(datum)
    return dataset
