import os
from vm import Machine


if __name__ == "__main__":

    with open(os.path.join("inputs", "day19.in")) as f:
        program = [int(opcode) for opcode in f.read().strip().split(",")]

    # First part - just apply brute force
    points_affected = 0
    for y in range(0, 50):
        for x in range(0, 50):
            machine = Machine(program, [x, y])
            machine.execute()
            points_affected += machine.output[0]
    assert points_affected == 121
