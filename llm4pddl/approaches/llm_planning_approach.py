"""An approach that uses the output of an LLM to guide planning."""

import logging
from typing import List, Optional, Tuple

from llm4pddl import utils
from llm4pddl.approaches.llm_open_loop_approach import LLMOpenLoopApproach
from llm4pddl.flags import FLAGS
from llm4pddl.structs import LLMResponse, Plan, Task, TaskMetrics


class LLMPlanningApproach(LLMOpenLoopApproach):
    """An approach that uses the output of an LLM to guide planning."""

    @property
    def is_planning_based(self) -> bool:
        return True

    def get_name(self) -> str:
        return "llm-plan"

    def _llm_responses_to_plan(
            self, responses: List[LLMResponse],
            task: Task) -> Tuple[Optional[Plan], TaskMetrics]:
        # Turn each response into a sequence of actions. Do not check the
        # preconditions of the actions; rely on the planner to do that.
        partial_plans = []
        for response in responses:
            logging.debug(f"Processing response:\n{response.response_text}")
            partial_plan = self._llm_response_to_plan(response, task)
            partial_plans.append(partial_plan)
        # Use the partial plans to guide the planner.
        return utils.run_pyperplan_planning(
            task,
            partial_plans=partial_plans,
            partial_plan_guidance_method=FLAGS.llm_plan_guidance_method)
