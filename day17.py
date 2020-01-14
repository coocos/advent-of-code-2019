import os
import collections
from operator import attrgetter
from typing import List, DefaultDict

from vm import Machine

Vec = collections.namedtuple("Vec", ["x", "y"])


def create_grid(data: List[int]) -> DefaultDict[Vec, str]:

    grid: DefaultDict[Vec, str] = collections.defaultdict(str)

    y = 0
    x = 0
    for d in data:
        if chr(d) == "\n":
            y += 1
            x = 0
        else:
            grid[Vec(x, y)] = chr(d)
            x += 1

    xs = [vec.x for vec in sorted(grid.keys(), key=attrgetter("x"))]
    ys = [vec.y for vec in sorted(grid.keys(), key=attrgetter("y"))]

    for y in range(ys[0], ys[-1] + 1):
        row = ""
        for x in range(xs[0], xs[-1] + 1):
            row += grid[Vec(x, y)]
        print("".join(row))

    return grid


def alignment_paremeter_sum(grid: DefaultDict[Vec, str]) -> int:

    xs = [vec.x for vec in sorted(grid.keys(), key=attrgetter("x"))]
    ys = [vec.y for vec in sorted(grid.keys(), key=attrgetter("y"))]

    intersections = []
    for y in range(ys[0] + 1, ys[-1] - 1):
        for x in range(xs[0] + 1, xs[-1] - 1):
            if (
                grid[Vec(x, y)] == "#"
                and grid[Vec(x + 1, y)] == "#"
                and grid[Vec(x - 1, y)] == "#"
                and grid[Vec(x, y + 1)] == "#"
                and grid[Vec(x, y - 1)] == "#"
            ):
                intersections.append(Vec(x, y))

    return sum(vec.x * vec.y for vec in intersections)


if __name__ == "__main__":

    with open(os.path.join("inputs", "day17.in")) as f:
        program = [int(instruction) for instruction in f.read().strip().split(",")]

    # First part
    machine = Machine(program, [], wait_for_input=True)
    machine.execute()

    grid = create_grid(machine.output)
    assert alignment_paremeter_sum(grid) == 3292
