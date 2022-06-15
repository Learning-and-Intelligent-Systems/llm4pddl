"""Approaches module."""

from llm4pddl.src.approaches.base_approach import BaseApproach


def create_approach(approach_name: str) -> BaseApproach:
    """Create a new approach instance."""
    import ipdb; ipdb.set_trace()