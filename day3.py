import collections
from typing import List, Set, Dict


Vec = collections.namedtuple("Vec", ["x", "y"])


if __name__ == "__main__":

    with open("day3.in") as f:
        wires = [line.strip().split(",") for line in f.readlines()]

    # Map of direction literals to vectors
    vecs = {"U": Vec(0, 1), "R": Vec(1, 0), "D": Vec(0, -1), "L": Vec(-1, 0)}
    # Sets of points formed by the two wires
    points: List[Set] = [set() for _ in wires]
    # Map how many steps it takes to reach a point
    steps: List[Dict[Vec, int]] = [{} for _ in wires]

    origin = Vec(0, 0)

    for i, wire in enumerate(wires):

        step = 0
        pos = origin

        for path in wire:

            direction, length = path[0], int(path[1:])

            for l in range(1, length + 1):
                current = Vec(
                    pos.x + vecs[direction].x * l, pos.y + vecs[direction].y * l,
                )
                points[i].add(current)
                step += 1
                steps[i][current] = step

            pos = current

    crosses = points[0] & points[1]

    # First part
    closest_manhattan = sorted(
        [abs(origin.x - c.x) + abs(origin.y - c.y) for c in crosses]
    )[0]
    assert closest_manhattan == 1431

    # Second part
    closest_step = sorted([steps[0][c] + steps[1][c] for c in crosses])[0]
    assert closest_step == 48012
