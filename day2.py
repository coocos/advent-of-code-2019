import os
import sys
from typing import List
from enum import Enum


class IntcodeException(Exception):
    pass


class Opcode(Enum):

    ADD = 1
    MULTIPLY = 2
    HALT = 99


def execute(program: List[int]) -> List[int]:

    pointer = 0
    opcode = Opcode(program[pointer])

    while opcode != Opcode.HALT:

        a, b, c = program[pointer + 1 : pointer + 4]

        if opcode == Opcode.ADD:
            program[c] = program[a] + program[b]
        elif opcode == Opcode.MULTIPLY:
            program[c] = program[a] * program[b]
        else:
            raise IntcodeException(f"Unhandled instruction {opcode}")

        pointer += 4
        opcode = Opcode(program[pointer])

    return program


if __name__ == "__main__":

    with open(os.path.join("inputs", "day2.in")) as f:
        program = [int(code) for code in f.read().split(",")]

    # First part
    copy = program[:]
    copy[1] = 12
    copy[2] = 2
    executed = execute(copy)
    assert executed[0] == 3409710

    # Second part
    for noun in range(100):
        for verb in range(100):
            copy = program[:]
            copy[1] = noun
            copy[2] = verb
            executed = execute(copy)
            if executed[0] == 19690720:
                assert 100 * noun + verb == 7912
                sys.exit()

    assert False
