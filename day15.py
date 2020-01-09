import os
import time
import collections
from enum import IntEnum
from vm import Machine

Vec = collections.namedtuple("Vec", ["x", "y"])
direction_map = {1: Vec(0, -1), 2: Vec(0, 1), 3: Vec(-1, 0), 4: Vec(1, 0)}


class Direction(IntEnum):

    NORTH = 1
    SOUTH = 2
    WEST = 3
    EAST = 4


def explore(position, previous, machine, grid):

    machine.execute()
    tile = machine.output[-1]

    # Ran into a wall - terminate recursion
    if tile == 0:
        grid[position] = "#"
        return
    elif tile == 1:
        grid[position] = "."
    else:
        grid[position] = "o"

    if os.getenv("PRETTY_AOC"):
        os.system("clear")
        draw_grid(grid, position)
        time.sleep(0.01)

    for d in (1, 2, 3, 4):
        vec = direction_map[d]

        next_position = Vec(position.x + vec.x, position.y + vec.y)
        if next_position != previous:

            # Step to the direction
            machine.inputs.append(d)
            explore(next_position, position, machine, grid)

            # Now reverse back again
            if grid[next_position] != "#":
                reverse_d = {1: 2, 2: 1, 3: 4, 4: 3}[d]
                machine.inputs.append(reverse_d)
                machine.execute()


def distance_to_oxygen(grid, start_pos):

    queue = collections.deque([(1, start_pos)])
    visited = set()

    while queue:

        distance, pos = queue.popleft()

        if grid[pos] == "o":
            return distance
        elif grid[pos] == "#":
            continue

        visited.add(pos)

        for vec in direction_map.values():
            next_pos = Vec(pos.x + vec.x, pos.y + vec.y)
            if next_pos not in visited:
                queue.append((distance + 1, next_pos))


def minutes_for_oxygen_to_spread(grid, oxygen_pos):

    queue = collections.deque([(0, oxygen_pos)])
    visited = set()

    while queue:

        minutes, pos = queue.popleft()
        visited.add(pos)

        for vec in direction_map.values():
            next_pos = Vec(pos.x + vec.x, pos.y + vec.y)
            if next_pos not in visited and grid[next_pos] != "#":
                queue.append((minutes + 1, next_pos))

    return minutes


def draw_grid(grid, position) -> None:

    ys = [vec.y for vec in sorted(grid.keys(), key=lambda pos: pos.y)]
    xs = [vec.x for vec in sorted(grid.keys(), key=lambda pos: pos.x)]

    for y in range(ys[0], ys[-1] + 1):
        row = []
        for x in range(xs[0], xs[-1] + 1):
            if Vec(x, y) == position:
                row.append("x")
            elif Vec(x, y) == Vec(0, 0):
                row.append("s")
            else:
                row.append(grid[Vec(x, y)])
        print("".join(row))


if __name__ == "__main__":

    with open(os.path.join("inputs", "day15.in")) as f:
        program = [int(instr) for instr in f.read().strip().split(",")]

    # First part
    machine = Machine(program, [], wait_for_input=True)
    machine.execute()

    grid = collections.defaultdict(lambda: " ")

    # Map the unknown part of the ship using depth-first search
    machine.inputs.append(Direction.SOUTH)
    start_pos = Vec(0, 0)
    explore(start_pos, None, machine, grid)
    os.system("clear")
    draw_grid(grid, start_pos)

    # Use breadth-first search to find the shortest path to oxygen
    distance = distance_to_oxygen(grid, start_pos)
    assert distance == 300

    # Second part
    oxygen_pos = None
    for pos, point in grid.items():
        if point == "o":
            oxygen_pos = pos
            break
    assert oxygen_pos is not None

    # Use breadth-first search again to find the path to the most distant point
    minutes = minutes_for_oxygen_to_spread(grid, oxygen_pos)
    assert minutes == 312
