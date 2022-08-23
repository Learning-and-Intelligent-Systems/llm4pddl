"""A meta-approach that uses model-predictive control with another approach."""

import logging
from typing import List, Optional, Tuple

from llm4pddl import utils
from llm4pddl.approaches.base_approach import BaseApproach
from llm4pddl.flags import FLAGS
from llm4pddl.structs import Dataset, Plan, Task, TaskMetrics


class MPCApproach(BaseApproach):
    """Wraps another approach and uses model-predictive-control."""

    def __init__(self, wrapped_approach: BaseApproach) -> None:
        super().__init__()
        self._wrapped_approach = wrapped_approach

    @property
    def is_learning_based(self) -> bool:
        return self._wrapped_approach.is_learning_based

    @property
    def is_planning_based(self) -> bool:
        return self._wrapped_approach.is_planning_based

    def get_name(self) -> str:
        return f"mpc-{self.wrapped_approach.get_name()}"

    def solve(self, task: Task) -> Tuple[Optional[Plan], TaskMetrics]:
        raise NotImplementedError("Override me!")

    def train(self, dataset: Dataset) -> None:
        return self._wrapped_approach.train(dataset)