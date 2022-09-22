"""An approach that samples random applicable actions."""

from typing import Optional, Tuple

from llm4pddl import utils
from llm4pddl.approaches.base_approach import BaseApproach
from llm4pddl.flags import FLAGS
from llm4pddl.structs import Plan, Task, TaskMetrics


class RandomActionsApproach(BaseApproach):
    """An approach that samples random applicable actions."""

    @property
    def is_learning_based(self) -> bool:
        return False

    @property
    def is_planning_based(self) -> bool:
        return False

    def get_name(self) -> str:
        return "random-actions"

    def solve(self, task: Task) -> Tuple[Optional[Plan], TaskMetrics]:
        metrics: TaskMetrics = {}
        plan = utils.get_random_partial_plan(task,
                                             self._rng,
                                             FLAGS.random_actions_max_steps,
                                             timeout=FLAGS.planning_timeout)
        return plan, metrics
