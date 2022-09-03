"""Domain-specific plan creation."""

from collections import defaultdict
from typing import Collection, Dict, List, Set

from llm4pddl import utils
from llm4pddl.structs import Plan, PyperplanObject, PyperplanPredicate, Task


def create_manual_plan(task: Task) -> Plan:
    """Generate a plan for the task using env-specific code."""
    if "blocks" in task.task_id.lower():
        return _create_manual_blocks_plan(task)
    if "miconic" in task.task_id.lower():
        return _create_manual_miconic_plan(task)
    if "logistics" in task.task_id.lower():
        return _create_manual_logistics_plan(task)
    assert "gripper" in task.task_id.lower()
    return _create_manual_gripper_plan(task)


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


def _create_manual_miconic_plan(task: Task) -> Plan:
    _, problem = utils.parse_task(task)

    # Parse the passengers and floors.
    floor_to_above_floors = defaultdict(set)
    passenger_to_origin = {}
    passenger_to_dest = {}
    lift_origin = None
    for atom in problem.initial_state:
        if atom.name.lower() == "above":
            (below, _), (above, _) = atom.signature
            floor_to_above_floors[below].add(above)
        elif atom.name.lower() == "origin":
            (passenger, _), (origin, _) = atom.signature
            passenger_to_origin[passenger] = origin
        elif atom.name.lower() == "destin":
            (passenger, _), (dest, _) = atom.signature
            passenger_to_dest[passenger] = dest
        elif atom.name.lower() == "lift-at":
            (lift_origin, _), = atom.signature
    assert lift_origin is not None

    # Construct the plan. Serve passengers one at a time, in lexicographic
    # order. Not a very efficient elevator, but a simple policy.
    plan = []

    remaining_passengers = sorted(passenger_to_dest)
    current_lift_loc = lift_origin
    next_lift_dest = None

    def _get_move_action(start: str, end: str) -> str:
        assert start != end
        if end in floor_to_above_floors[start]:
            return "up"
        return "down"

    while remaining_passengers:
        passenger = remaining_passengers.pop(0)
        # Move to pick up the passenger.
        next_lift_dest = passenger_to_origin[passenger]
        move = _get_move_action(current_lift_loc, next_lift_dest)
        plan.append(f"({move} {current_lift_loc} {next_lift_dest})")
        current_lift_loc = next_lift_dest
        # Board the passenger.
        plan.append(f"(board {current_lift_loc} {passenger})")
        # Move to the passenger's destination.
        next_lift_dest = passenger_to_dest[passenger]
        move = _get_move_action(current_lift_loc, next_lift_dest)
        plan.append(f"({move} {current_lift_loc} {next_lift_dest})")
        current_lift_loc = next_lift_dest
        # Drop off the passenger.
        plan.append(f"(depart {current_lift_loc} {passenger})")

    return plan


def _create_manual_logistics_plan(task: Task) -> Plan:
    _, problem = utils.parse_task(task)

    # Parse the problem.
    def _atoms_to_ats(
        atoms: Collection[PyperplanPredicate]
    ) -> Dict[PyperplanObject, PyperplanObject]:
        ats = {}
        for atom in atoms:
            if atom.name.lower() != "at":
                continue
            (vehicle, _), (loc, _) = atom.signature
            ats[vehicle] = loc
        return ats

    init_ats = _atoms_to_ats(problem.initial_state)
    goal_ats = _atoms_to_ats(problem.goal)
    pos_to_city = {}
    objects = problem.objects
    trucks = {o for o in objects if objects[o].name == "truck"}
    airports = {o for o in objects if objects[o].name == "airport"}
    packages = {o for o in objects if objects[o].name == "package"}
    airplanes = {o for o in objects if objects[o].name == "airplane"}
    assert set(goal_ats).issubset(packages)
    for atom in problem.initial_state:
        if atom.name.lower() != "in-city":
            continue
        (loc, _), (city, _) = atom.signature
        pos_to_city[loc] = city
    truck_to_city = {truck: pos_to_city[init_ats[truck]] for truck in trucks}
    airport_to_city = {airport: pos_to_city[airport] for airport in airports}
    # We only need one truck and airport per city.
    assert len(truck_to_city) == len(set(truck_to_city.values()))
    city_to_truck = {c: t for t, c in truck_to_city.items()}
    assert len(airport_to_city) == len(set(airport_to_city.values()))
    city_to_airport = {c: a for a, c in airport_to_city.items()}
    # We'll only ever use one airplane to keep the policy simple.
    airplane = sorted(airplanes)[0]

    # Construct the plan.
    plan = []

    # Process packages one at a time.
    current_ats = init_ats.copy()

    def _get_truck_subplan(package: str, truck: str, city: str,
                           package_dest: str) -> Plan:
        # Note that current_ats is used and updated internally.
        assert pos_to_city[package_dest] == city
        subplan = []
        # Move the truck to the package init.
        package_init = current_ats[package]
        truck_init = current_ats[truck]
        subplan.append(f"(drive-truck {truck} {truck_init} "
                       f"{package_init} {city})")
        current_ats[truck] = package_init
        # Load the truck.
        subplan.append(f"(load-truck {package} {truck} {package_init})")
        # Drive the truck to the package dest.
        subplan.append(f"(drive-truck {truck} {package_init} "
                       f"{package_dest} {city})")
        current_ats[truck] = package_dest
        # Unload the truck.
        subplan.append(f"(unload-truck {package} {truck} {package_dest})")
        current_ats[package] = package_dest
        return subplan

    def _get_plane_subplan(package: str, plane: str, init_airport: str,
                           dest_airport: str) -> Plan:
        # Note that current_ats is used and updated internally.
        assert init_airport != dest_airport
        assert current_ats[package] == init_airport
        subplan = []
        # Fly the plane to the init airport.
        plane_init = current_ats[plane]
        subplan.append(f"(fly-airplane {plane} {plane_init} {init_airport})")
        current_ats[plane] = init_airport
        # Load the plane.
        subplan.append(f"(load-airplane {package} {plane} {init_airport})")
        # Fly the plane to the dest airport.
        subplan.append(f"(fly-airplane {plane} {init_airport} {dest_airport})")
        current_ats[plane] = dest_airport
        # Unload the plane.
        subplan.append(f"(unload-airplane {package} {plane} {dest_airport})")
        current_ats[package] = dest_airport
        return subplan

    for package in sorted(goal_ats):
        package_init = current_ats[package]
        package_dest = goal_ats[package]
        init_city = pos_to_city[package_init]
        dest_city = pos_to_city[package_dest]
        # If the package is not yet in the goal city, we need to fly it.
        if init_city != dest_city:
            # If the package is not yet at an airport, we need to deliver it.
            if package_init not in airports:
                truck = city_to_truck[init_city]
                port = city_to_airport[init_city]
                subplan = _get_truck_subplan(package, truck, init_city, port)
                plan.extend(subplan)
                package_init = port
            # Now that the package is at an airport, we need to fly it.
            dest_airport = city_to_airport[dest_city]
            subplan = _get_plane_subplan(package, airplane, package_init,
                                         dest_airport)
            plan.extend(subplan)
            package_init = dest_airport
        # If the package is not yet at its destination, we need to drive it.
        if package_init != package_dest:
            truck = city_to_truck[dest_city]
            subplan = _get_truck_subplan(package, truck, dest_city,
                                         package_dest)
            plan.extend(subplan)

    return plan
