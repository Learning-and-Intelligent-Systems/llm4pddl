"""Approaches module."""

from llm4pddl.approaches.base_approach import BaseApproach
from llm4pddl.approaches.llm_open_loop_approach import LLMOpenLoopApproach
from llm4pddl.approaches.llm_planning_approach import LLMPlanningApproach
from llm4pddl.approaches.pure_planning_approach import PurePlanningApproach
from llm4pddl.flags import FLAGS


def create_approach(approach_name: str) -> BaseApproach:
    """Create an approach."""
    if approach_name == "pure-planning":
        return PurePlanningApproach()
    if approach_name == "llm-standard":
        return LLMOpenLoopApproach(num_completions=1, temperature=0.0)
    if approach_name == "llm-multi":
        return LLMOpenLoopApproach(
            num_completions=FLAGS.llm_multi_num_completions,
            temperature=FLAGS.llm_multi_temperature)
    if approach_name == "llm-standard-plan":
        return LLMPlanningApproach(num_completions=1, temperature=0.0)
    if approach_name == "llm-multi-plan":
        return LLMPlanningApproach(
            num_completions=FLAGS.llm_multi_num_completions,
            temperature=FLAGS.llm_multi_temperature)
    raise NotImplementedError(f"Unrecognized approach name: {approach_name}")
