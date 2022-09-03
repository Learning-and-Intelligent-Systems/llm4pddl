"""An approach that runs env-specific code from manual_planning.py."""

from typing import Optional, Tuple

from llm4pddl.approaches.base_approach import BaseApproach
from llm4pddl.manual_planning import create_manual_plan
from llm4pddl.structs import Plan, Task, TaskMetrics


class ManualPlanningApproach(BaseApproach):
    """An approach that runs env-specific code from manual_planning.py."""

    @property
    def is_learning_based(self) -> bool:
        return False

    @property
    def is_planning_based(self) -> bool:
        return False

    def get_name(self) -> str:
        return "manual-planning"

    def solve(self, task: Task) -> Tuple[Optional[Plan], TaskMetrics]:
        metrics: TaskMetrics = {}
        plan = create_manual_plan(task)
        return plan, metrics
