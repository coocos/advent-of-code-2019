import os
import sys
from vm import Machine


if __name__ == "__main__":

    with open(os.path.join("inputs", "day2.in")) as f:
        program = [int(code) for code in f.read().split(",")]

    # First part
    copy = program[:1] + [12, 2] + program[3:]
    machine = Machine(copy, [])
    machine.execute()
    assert machine.memory[0] == 3409710

    # Second part
    for noun in range(100):
        for verb in range(100):
            copy = program[:1] + [noun, verb] + program[3:]
            machine = Machine(copy, [])
            machine.execute()
            if machine.memory[0] == 19690720:
                assert 100 * noun + verb == 7912
                sys.exit()

    assert False
