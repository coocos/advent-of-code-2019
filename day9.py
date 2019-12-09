import os
from vm import Machine


if __name__ == "__main__":

    with open(os.path.join("inputs", "day9.in")) as f:
        boost = [int(instruction) for instruction in f.read().strip().split(",")]

    machine = Machine(boost, [1])
    machine.execute()
    assert machine.output == [2406950601]

    machine = Machine(boost, [2])
    machine.execute()
    assert machine.output == [83239]
