"""Approaches module."""

from llm4pddl.approaches.base_approach import BaseApproach
from llm4pddl.approaches.llm_approaches import LLMOpenLoopApproach
from llm4pddl.approaches.pure_planning_approach import PurePlanningApproach


def create_approach(approach_name: str) -> BaseApproach:
    """Create an approach."""
    if approach_name == "pure-planning":
        return PurePlanningApproach()
    if approach_name == "llm-standard":
        return LLMOpenLoopApproach(num_completions=1, temperature=0.0)
    raise NotImplementedError(f"Unrecognized approach name: {approach_name}")
