import os
from typing import List
from vm import Machine


def point_in_beam(program: List[int], x: int, y: int) -> bool:

    machine = Machine(program, [x, y])
    machine.execute()
    return bool(machine.output[0])


if __name__ == "__main__":

    with open(os.path.join("inputs", "day19.in")) as f:
        program = [int(opcode) for opcode in f.read().strip().split(",")]

    # First part - just apply brute force and iterate over all the points
    points_affected = 0
    for y in range(0, 50):
        for x in range(0, 50):
            if point_in_beam(program, x, y):
                points_affected += 1
    assert points_affected == 121

    # Second part - find the position of the square by locating the closest
    # point (x, y) inside the beam for which the point (x + 99, y - 99)
    # is also inside the beam. Those two points form the closest square.
    previous_x = 0
    top_left = None

    for y in range(0, 10_000):

        if top_left:
            break

        for x in range(previous_x, 10_000):
            if point_in_beam(program, x, y):

                # The beam will start more to the right on the next row
                # so then you can skip the first (previous_x - 1) points
                previous_x = x

                # The point 100 points to the right and 100 points above
                # is inside the beam so this position is the bottom-left
                # corner of the square
                if y >= 100 and point_in_beam(program, x + 99, y - 99):
                    top_left = (x, y - 99)
                    break
                break

    assert top_left == (1509, 773)
