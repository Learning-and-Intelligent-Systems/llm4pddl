"""Domain-specific plan creation."""

from llm4pddl.envs.base_env import BaseEnv
from llm4pddl.structs import Task, Plan
from llm4pddl import utils


def create_manual_plan(task: Task, env: BaseEnv) -> Plan:
    """Generate a plan for the task using env-specific code."""
    
    assert "blocks" in env
    return _create_manual_blocks_plan(task)


def _create_manual_blocks_plan(task: Task) -> Plan:
    _, problem = utils.parse_task(task)
    import ipdb; ipdb.set_trace()

