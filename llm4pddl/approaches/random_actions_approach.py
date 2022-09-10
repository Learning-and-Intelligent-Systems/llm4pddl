"""An approach that samples random applicable actions."""

import logging
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
        pyperplan_task = utils.get_pyperplan_task(task)
        current_facts = pyperplan_task.initial_state
        plan = []
        for t in range(FLAGS.random_actions_max_steps):
            # Sort for determinism.
            applicable_action_set = {
                o
                for o in pyperplan_task.operators
                if o.applicable(current_facts)
            }
            applicable_actions = sorted(applicable_action_set,
                                        key=lambda o: o.name)
            # Dead end.
            if not applicable_actions:
                logging.debug(f"Reached dead end on step {t}.")
                break
            # Sample an applicable action.
            action_idx = self._rng.choice(len(applicable_actions))
            action = applicable_actions[action_idx]
            # Extend the plan.
            plan.append(action.name)
            # Advance the state.
            current_facts = action.apply(current_facts)
            # Check the plan at each step.
            if utils.validate_plan(task, plan, verbose=False):
                # Success!
                logging.debug(f"Found a plan on step {t}.")
                return plan, metrics
        # Failed.
        logging.debug("Random actions approach failed to find a plan.")
        return None, metrics
