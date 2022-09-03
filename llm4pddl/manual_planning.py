"""Domain-specific plan creation."""

from typing import Collection, Dict, List, Set

from llm4pddl import utils
from llm4pddl.structs import Plan, PyperplanObject, PyperplanPredicate, Task


def create_manual_plan(task: Task, env_name: str) -> Plan:
    """Generate a plan for the task using env-specific code."""
    if "blocks" in env_name:
        return _create_manual_blocks_plan(task)
    if "gripper" in env_name:
        return _create_manual_gripper_plan(task)
    raise NotImplementedError(f"Manual plan not implemented for {env_name}")


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


def _create_manual_gripper_plan(task: Task) -> Plan:
    _, problem = utils.parse_task(task)

    # Parse the balls.
    def _atoms_to_ball_locs(
            atoms: Collection[PyperplanPredicate]) -> Dict[str, str]:
        ball_to_loc = {}
        for atom in atoms:
            if atom.name.lower() != "at":
                continue
            (ball, _), (loc, _) = atom.signature
            ball_to_loc[ball] = loc
        return ball_to_loc

    # Parse the grippers.
    def _atoms_to_grippers(atoms: Collection[PyperplanPredicate]) -> Set[str]:
        free_grippers = set()
        all_grippers = set()
        for atom in atoms:
            if atom.name.lower() == "free":
                (gripper, _), = atom.signature
                free_grippers.add(gripper)
            elif atom.name.lower() == "gripper":
                (gripper, _), = atom.signature
                all_grippers.add(gripper)
        # Assume all grippers start out free.
        assert free_grippers == all_grippers
        return all_grippers

    # Parse the robot.
    def _atoms_to_robot_loc(atoms: Collection[PyperplanPredicate]) -> str:
        at_robby = [a for a in atoms if a.name.lower() == "at-robby"]
        assert len(at_robby) == 1
        return at_robby[0].signature[0][0]

    # Assumes that all balls start out in the same place.
    init_ball_locs = _atoms_to_ball_locs(problem.initial_state)
    assert len(init_ball_locs) > 0
    init_ball_loc = next(iter(init_ball_locs.values()))
    assert all(l == init_ball_loc for l in init_ball_locs.values())
    grippers = sorted(_atoms_to_grippers(problem.initial_state))
    robot_loc = _atoms_to_robot_loc(problem.initial_state)
    assert robot_loc == init_ball_loc
    # Assumes that all goal balls need to go to the same place.
    goal_ball_locs = _atoms_to_ball_locs(problem.goal)
    goal_ball_loc = next(iter(goal_ball_locs.values()))
    assert all(l == goal_ball_loc for l in goal_ball_locs.values())

    # Construct the plan.
    plan = []

    remaining_balls = sorted(goal_ball_locs)
    while remaining_balls:
        gripper_to_ball = {}
        for gripper in grippers:
            if not remaining_balls:  # pragma: no cover
                break
            gripper_to_ball[gripper] = remaining_balls.pop(0)
        # Picks.
        for gripper in sorted(gripper_to_ball):
            ball = gripper_to_ball[gripper]
            plan.append(f"(pick {ball} {init_ball_loc} {gripper})")
        # Move.
        plan.append(f"(move {init_ball_loc} {goal_ball_loc})")
        # Place.
        for gripper in sorted(gripper_to_ball):
            ball = gripper_to_ball[gripper]
            plan.append(f"(drop {ball} {goal_ball_loc} {gripper})")
        # If there are more to go, move back.
        if remaining_balls:
            plan.append(f"(move {goal_ball_loc} {init_ball_loc})")

    return plan
