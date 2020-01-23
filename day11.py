from __future__ import annotations

import os
import collections
from vm import Machine
from dataclasses import dataclass
from enum import IntEnum, unique
from operator import attrgetter
from typing import List, DefaultDict


Vector = collections.namedtuple("Vector", ["x", "y"])


@unique
class Panel(IntEnum):

    BLACK: int = 0
    WHITE: int = 1


@dataclass
class Robot:

    pos: Vector = Vector(0, 0)
    dir: Vector = Vector(0, 1)

    def turn_left(self) -> None:

        if self.dir == Vector(0, 1):
            self.dir = Vector(-1, 0)
        elif self.dir == Vector(-1, 0):
            self.dir = Vector(0, -1)
        elif self.dir == Vector(0, -1):
            self.dir = Vector(1, 0)
        else:
            self.dir = Vector(0, 1)

        self.pos = Vector(self.pos.x + self.dir.x, self.pos.y + self.dir.y)

    def turn_right(self) -> None:

        if self.dir == Vector(0, 1):
            self.dir = Vector(1, 0)
        elif self.dir == Vector(1, 0):
            self.dir = Vector(0, -1)
        elif self.dir == Vector(0, -1):
            self.dir = Vector(-1, 0)
        else:
            self.dir = Vector(0, 1)

        self.pos = Vector(self.pos.x + self.dir.x, self.pos.y + self.dir.y)


def paint_panels(
    program: List[int], starting_panel: Panel
) -> DefaultDict[Vector, Panel]:

    robot = Robot()
    panels: DefaultDict[Vector, Panel] = collections.defaultdict(lambda: Panel.BLACK)

    panels[robot.pos] = starting_panel
    input_stream: List[int] = [panels[robot.pos]]
    machine = Machine(program, input_stream, pause_on_output=True)

    while not machine.halted:

        machine.execute()
        machine.execute()

        if machine.halted:
            break

        direction = machine.output.pop()
        panel = Panel(machine.output.pop())
        panels[robot.pos] = panel

        if direction == 0:
            robot.turn_left()
        else:
            robot.turn_right()

        input_stream.append(panels[robot.pos])

    return panels


if __name__ == "__main__":

    with open(os.path.join("inputs", "day11.in")) as f:
        program = [int(byte) for byte in f.read().strip().split(",")]

    # First part
    panels = paint_panels(program, Panel.BLACK)
    assert len(panels) == 2016

    # Second part
    panels = paint_panels(program, Panel.WHITE)

    xs = sorted(panels.keys(), key=attrgetter("x"))
    ys = sorted(panels.keys(), key=attrgetter("y"))

    for y in reversed(range(ys[0].y, ys[-1].y + 1)):
        buf = ""
        for x in range(xs[0].x, xs[-1].x + 1):
            buf += "#" if panels[Vector(x, y)] else " "
        print(buf)
