"""Approaches module."""

from llm4pddl.approaches.base_approach import BaseApproach
from llm4pddl.approaches.pure_planning_approach import PurePlanningApproach
from llm4pddl.approaches.llm_approaches import LLMOpenLoopApproach


def create_approach(approach_name: str) -> BaseApproach:
    """Create an approach."""
    if approach_name == "pure-planning":
        return PurePlanningApproach()
    if approach_name == "llm-open-loop":
        return LLMOpenLoopApproach()
    raise NotImplementedError(f"Unrecognized approach name: {approach_name}")
