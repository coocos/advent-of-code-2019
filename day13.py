import os
from enum import IntEnum, unique
from vm import Machine


@unique
class Tile(IntEnum):

    EMPTY: int = 0
    WALL: int = 1
    BLOCK: int = 2
    PADDLE: int = 3
    BALL: int = 4

    def display(self) -> str:
        return {0: " ", 1: "#", 2: "*", 3: "=", 4: "o"}[self]


if __name__ == "__main__":

    with open(os.path.join("inputs", "day13.in")) as f:
        program = [int(instr) for instr in f.read().strip().split(",")]

    # First part
    machine = Machine(program, [])
    machine.execute()

    output = machine.output[:]
    pixels = {}

    while output:
        x, y, tile = output[:3]
        output = output[3:]
        pixels[(x, y)] = Tile(tile)

    assert sum(1 for tile in pixels.values() if tile is Tile.BLOCK) == 361

    for y in range(22 + 1):
        row = ""
        for x in range(42 + 1):
            row += pixels[(x, y)].display()
        print(row)
