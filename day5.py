import os
from vm import Machine


if __name__ == "__main__":

    with open(os.path.join("inputs", "day5.in")) as f:
        program = [int(opcode) for opcode in f.read().strip().split(",")]

    # First part
    machine = Machine(program, [1])
    machine.execute()
    assert machine.output == [0, 0, 0, 0, 0, 0, 0, 0, 0, 12428642]

    # Second part
    machine = Machine(program, [5])
    machine.execute()
    assert machine.output == [918655]
