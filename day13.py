import os
from enum import IntEnum, unique
from vm import Machine
from typing import Tuple, Dict


@unique
class Tile(IntEnum):

    EMPTY: int = 0
    WALL: int = 1
    BLOCK: int = 2
    PADDLE: int = 3
    BALL: int = 4

    def display(self) -> str:
        return {0: " ", 1: "#", 2: "*", 3: "=", 4: "o"}[self]


Pixels = Dict[Tuple[int, int], Tile]


def draw(pixels: Pixels, score: int) -> None:

    for y in range(22 + 1):
        row = ""
        for x in range(42 + 1):
            row += pixels[(x, y)].display()
        print(row)
    print(f"Score: {score}")


if __name__ == "__main__":

    with open(os.path.join("inputs", "day13.in")) as f:
        program = [int(instr) for instr in f.read().strip().split(",")]

    # First part
    machine = Machine(program, [])
    machine.execute()

    output = machine.output[:]
    pixels: Pixels = {}

    while output:
        x, y, tile = output[:3]

        # Special score instruction
        if x == -1 and y == 0:
            continue

        output = output[3:]
        pixels[(x, y)] = Tile(tile)

    assert sum(1 for tile in pixels.values() if tile is Tile.BLOCK) == 361

    # Second part
    machine = Machine(program, [], wait_for_input=True)
    machine.memory[0] = 2

    pixels = {}
    score = 0

    # First draw until input is requested so that all tiles are visible
    machine.execute()

    while machine.output:
        x, y, tile = machine.output[:3]
        if (x, y) == (-1, 0):
            score = tile
        else:
            pixels[(x, y)] = Tile(tile)
        machine.output = machine.output[3:]

    draw(pixels, score)

    # Start playing the game
    machine.inputs.append(0)
    ball = 0
    paddle = 0
    player_input = 0

    while not machine.halted:
        machine.execute()
        while machine.output:
            x, y, tile = machine.output[:3]
            if (x, y) == (-1, 0):
                score = tile
            else:
                if tile == Tile.BALL:
                    ball = x
                elif tile == Tile.PADDLE:
                    paddle = x
                pixels[(x, y)] = Tile(tile)
            machine.output = machine.output[3:]

        # Simply move the paddle towards the ball
        player_input = -1 if ball < paddle else 1

        machine.inputs.append(player_input)

    assert score == 17590
