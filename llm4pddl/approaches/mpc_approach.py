"""A meta-approach that uses model-predictive control with another approach."""

from typing import Optional, Tuple

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
        return f"mpc-{self._wrapped_approach.get_name()}"

    def solve(self, task: Task) -> Tuple[Optional[Plan], TaskMetrics]:
        executed_actions: Plan = []
        original_task = task
        current_task = task
        cumulative_metrics: TaskMetrics = {}

        for _ in range(FLAGS.mpc_max_steps):
            # Check if the task is solved.
            if utils.validate_plan(original_task, executed_actions):
                break

            # Call the wrapped approach.
            plan, metrics = self._wrapped_approach.solve(current_task)

            # Accumulate metrics.
            if not cumulative_metrics:
                cumulative_metrics = metrics.copy()
            else:
                for metric, value in metrics.items():
                    cumulative_metrics[metric] += value

            # If the wrapped approach failed to find any plan, give up.
            if not plan:
                return None, cumulative_metrics

            # Otherwise, try to "execute" the first step in the plan. This
            # returns None if the action is not applicable.
            act = plan.pop(0)
            executed_actions.append(act)
            next_task = utils.get_next_task_from_action(current_task, act)
            if next_task is None:
                return None, cumulative_metrics
            current_task = next_task

        return executed_actions, cumulative_metrics

    def train(self, dataset: Dataset) -> None:
        return self._wrapped_approach.train(dataset)
