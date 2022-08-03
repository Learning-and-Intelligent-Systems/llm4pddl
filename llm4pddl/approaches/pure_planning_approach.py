"""An approach that simply runs a planner to solve tasks."""

from typing import Optional

from llm4pddl import utils
from llm4pddl.approaches.base_approach import BaseApproach
from llm4pddl.structs import Plan, Task


class PurePlanningApproach(BaseApproach):
    """An approach that simply runs a planner to solve tasks."""

    @property
    def is_learning_based(self) -> bool:
        return False

    def get_name(self) -> str:
        return "pure-planning"

    def solve(self, task: Task) -> Optional[Plan]:
        return utils.run_planning(task)
