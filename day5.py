import os
from typing import List, Tuple
from enum import Enum


class IntcodeException(Exception):
    pass


class Opcode(Enum):

    ADD = 1
    MULTIPLY = 2
    SAVE = 3
    PRINT = 4
    JUMP_IF_TRUE = 5
    JUMP_IF_FALSE = 6
    LESS_THAN = 7
    EQUALS = 8
    HALT = 99


# TODO: Use dataclass?
class Instruction:
    def __init__(self, instruction: int):
        self.instruction = instruction
        self.opcode = Opcode(instruction % 100)

        # FIXME: This is nasty
        modes = str(instruction)[:-2]
        modes = "0" * (3 - len(modes)) + modes
        self.modes = [int(mode) for mode in reversed(modes)]

    def __repr__(self):
        return (
            f"Instruction: {self.instruction} Opcode: {self.opcode} Modes: {self.modes}"
        )


def execute(program: List[int], program_input: int = 0) -> Tuple[List[int], List[int]]:

    output: List[int] = []
    pointer = 0
    instruction = Instruction(program[pointer])

    while instruction.opcode != Opcode.HALT:

        if instruction.opcode == Opcode.ADD:
            a, b, c = program[pointer + 1 : pointer + 4]
            # FIXME: Don't repeat this everywhere
            a = a if instruction.modes[0] else program[a]
            b = b if instruction.modes[1] else program[b]
            program[c] = a + b
            pointer += 4
        elif instruction.opcode == Opcode.MULTIPLY:
            a, b, c = program[pointer + 1 : pointer + 4]
            a = a if instruction.modes[0] else program[a]
            b = b if instruction.modes[1] else program[b]
            program[c] = a * b
            pointer += 4
        elif instruction.opcode == Opcode.SAVE:
            a = program[pointer + 1]
            program[a] = program_input
            pointer += 2
        elif instruction.opcode == Opcode.PRINT:
            a = program[pointer + 1]
            msg = a if instruction.modes[0] else program[a]
            output.append(msg)
            print(msg)
            pointer += 2
        elif instruction.opcode == Opcode.JUMP_IF_TRUE:
            a, b = program[pointer + 1 : pointer + 3]
            a = a if instruction.modes[0] else program[a]
            b = b if instruction.modes[1] else program[b]
            if a != 0:
                pointer = b
            else:
                pointer += 3
        elif instruction.opcode == Opcode.JUMP_IF_FALSE:
            a, b = program[pointer + 1 : pointer + 3]
            a = a if instruction.modes[0] else program[a]
            b = b if instruction.modes[1] else program[b]
            if a == 0:
                pointer = b
            else:
                pointer += 3
        elif instruction.opcode == Opcode.LESS_THAN:
            a, b, c = program[pointer + 1 : pointer + 4]
            a = a if instruction.modes[0] else program[a]
            b = b if instruction.modes[1] else program[b]
            if a < b:
                program[c] = 1
            else:
                program[c] = 0
            pointer += 4
        elif instruction.opcode == Opcode.EQUALS:
            a, b, c = program[pointer + 1 : pointer + 4]
            a = a if instruction.modes[0] else program[a]
            b = b if instruction.modes[1] else program[b]
            if a == b:
                program[c] = 1
            else:
                program[c] = 0
            pointer += 4
        else:
            raise IntcodeException(f"Unhandled instruction {instruction}")

        instruction = Instruction(program[pointer])

    return program, output


if __name__ == "__main__":

    with open(os.path.join("inputs", "day5.in")) as f:
        program = [int(opcode) for opcode in f.read().strip().split(",")]

    # First part
    executed, output = execute(program[:], program_input=1)
    assert output == [0, 0, 0, 0, 0, 0, 0, 0, 0, 12428642]

    # Second part
    executed, output = execute(program[:], program_input=5)
    assert output == [918655]
