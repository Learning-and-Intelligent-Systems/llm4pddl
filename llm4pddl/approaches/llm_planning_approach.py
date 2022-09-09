"""An approach that uses the output of an LLM to guide planning."""

from typing import List, Optional, Tuple

from llm4pddl import utils
from llm4pddl.approaches.llm_open_loop_approach import LLMOpenLoopApproach
from llm4pddl.flags import FLAGS
from llm4pddl.structs import Plan, Task, TaskMetrics


class LLMPlanningApproach(LLMOpenLoopApproach):
    """An approach that uses the output of an LLM to guide planning."""

    @property
    def is_planning_based(self) -> bool:
        return True

    def get_name(self) -> str:
        return "llm-plan"

    def _solve_from_partial_plans(
            self, partial_plans: List[Plan],
            task: Task) -> Tuple[Optional[Plan], TaskMetrics]:
        # Use the partial plans to guide the planner.
        return utils.run_pyperplan_planning(
            task,
            partial_plans=partial_plans,
            partial_plan_guidance_method=FLAGS.llm_plan_guidance_method)
