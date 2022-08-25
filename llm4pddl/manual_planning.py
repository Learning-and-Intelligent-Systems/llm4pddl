"""Domain-specific plan creation."""

from typing import Collection, List

from llm4pddl import utils
from llm4pddl.structs import Plan, PyperplanObject, PyperplanPredicate, Task


def create_manual_plan(task: Task, env_name: str) -> Plan:
    """Generate a plan for the task using env-specific code."""

    assert "blocks" in env_name
    return _create_manual_blocks_plan(task)


def _create_manual_blocks_plan(task: Task) -> Plan:
    _, problem = utils.parse_task(task)

    # Parse the piles.
    def _atoms_to_piles(
            atoms: Collection[PyperplanPredicate]
    ) -> List[List[PyperplanObject]]:
        bottom_to_top_block = {}
        for atom in atoms:
            # Can't use ontable because it doesn't necessarily appear in goals.
            if atom.name.lower() != "on":
                continue
            (top, _), (bottom, _) = atom.signature
            bottom_to_top_block[bottom] = top
        # Infer the bottoms of piles.
        non_bottoms = set(bottom_to_top_block.values())
        pile_bottoms = set(bottom_to_top_block) - non_bottoms
        piles = []
        for bottom in sorted(pile_bottoms):
            pile = [bottom]
            while bottom in bottom_to_top_block:
                bottom = bottom_to_top_block[bottom]
                pile.append(bottom)
            piles.append(pile)
        return piles

    # Piles are bottom-to-top.
    init_piles = _atoms_to_piles(problem.initial_state)
    goal_piles = _atoms_to_piles(problem.goal)

    # Construct the plan.
    plan = []

    # Unstack first.
    for pile in init_piles:
        remaining_pile = list(pile)
        while len(remaining_pile) > 1:
            top = remaining_pile.pop()
            bottom = remaining_pile[-1]
            plan.append(f"(unstack {top} {bottom})")
            plan.append(f"(put-down {top})")

    # Now that all blocks are clear, start stacking the goal piles.
    for pile in goal_piles:
        remaining_pile = list(pile)
        while len(remaining_pile) > 1:
            bottom = remaining_pile.pop(0)
            top = remaining_pile[0]
            plan.append(f"(pick-up {top})")
            plan.append(f"(stack {top} {bottom})")

    return plan
