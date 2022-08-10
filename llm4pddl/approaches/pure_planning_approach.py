"""An approach that simply runs a planner to solve tasks."""

from typing import Optional, Tuple

from llm4pddl import utils
from llm4pddl.approaches.base_approach import BaseApproach
from llm4pddl.flags import FLAGS
from llm4pddl.structs import Plan, Task, TaskMetrics


class PurePlanningApproach(BaseApproach):
    """An approach that simply runs a planner to solve tasks."""

    @property
    def is_learning_based(self) -> bool:
        return False

    @property
    def is_planning_based(self) -> bool:
        return True

    def get_name(self) -> str:
        return "pure-planning"

    def solve(self, task: Task) -> Tuple[Optional[Plan], TaskMetrics]:
        return utils.run_planning(task, self._rng, planner=FLAGS.planner)
