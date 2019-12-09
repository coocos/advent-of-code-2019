from dataclasses import dataclass, field
from typing import List
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
    RELATIVE_BASE = 9
    HALT = 99


@dataclass
class Instruction:

    instruction: int
    opcode: Opcode = field(init=False)
    modes: List[int] = field(init=False)

    def __post_init__(self):
        self.opcode = Opcode(self.instruction % 100)
        self.modes = [
            self.instruction // 100 % 10,
            self.instruction // 1000 % 10,
            self.instruction // 10000 % 10,
        ]


@dataclass
class Machine:

    memory: List[int]
    inputs: List[int]
    ip: int = 0
    input_pointer: int = 0
    output: List[int] = field(default_factory=list)
    pause_on_output: bool = False
    relative_base: int = 0

    def __post_init__(self):
        self.memory = self.memory[:] + [0] * (2048 - len(self.memory))

    @property
    def halted(self) -> bool:
        return Instruction(self.memory[self.ip]).opcode == Opcode.HALT

    def param_value(self, mode, param):
        # Position mode
        if mode == 0:
            return self.memory[param]
        # Immediate mode
        elif mode == 1:
            return param
        # Relative mode
        elif mode == 2:
            return self.memory[self.relative_base + param]
        else:
            raise IntcodeException(f"Unknown mode {mode}")

    def execute(self) -> None:

        instruction = Instruction(self.memory[self.ip])

        while instruction.opcode != Opcode.HALT:

            if instruction.opcode == Opcode.ADD:
                a, b, c = self.memory[self.ip + 1 : self.ip + 4]
                a = self.param_value(instruction.modes[0], a)
                b = self.param_value(instruction.modes[1], b)
                if instruction.modes[2] == 2:
                    c = self.relative_base + c
                self.memory[c] = a + b
                self.ip += 4
            elif instruction.opcode == Opcode.MULTIPLY:
                a, b, c = self.memory[self.ip + 1 : self.ip + 4]
                a = self.param_value(instruction.modes[0], a)
                b = self.param_value(instruction.modes[1], b)
                if instruction.modes[2] == 2:
                    c = self.relative_base + c
                self.memory[c] = a * b
                self.ip += 4
            elif instruction.opcode == Opcode.SAVE:
                a = self.memory[self.ip + 1]
                if instruction.modes[0] == 2:
                    a = self.relative_base + a
                self.memory[a] = self.inputs[self.input_pointer]
                self.input_pointer += 1
                self.ip += 2
            elif instruction.opcode == Opcode.PRINT:
                a = self.memory[self.ip + 1]
                msg = self.param_value(instruction.modes[0], a)
                self.output.append(msg)
                self.ip += 2
                if self.pause_on_output:
                    return
            elif instruction.opcode == Opcode.JUMP_IF_TRUE:
                a, b = self.memory[self.ip + 1 : self.ip + 3]
                a = self.param_value(instruction.modes[0], a)
                b = self.param_value(instruction.modes[1], b)
                self.ip = b if a != 0 else self.ip + 3
            elif instruction.opcode == Opcode.JUMP_IF_FALSE:
                a, b = self.memory[self.ip + 1 : self.ip + 3]
                a = self.param_value(instruction.modes[0], a)
                b = self.param_value(instruction.modes[1], b)
                self.ip = b if a == 0 else self.ip + 3
            elif instruction.opcode == Opcode.LESS_THAN:
                a, b, c = self.memory[self.ip + 1 : self.ip + 4]
                a = self.param_value(instruction.modes[0], a)
                b = self.param_value(instruction.modes[1], b)
                if instruction.modes[2] == 2:
                    c = self.relative_base + c
                self.memory[c] = int(a < b)
                self.ip += 4
            elif instruction.opcode == Opcode.EQUALS:
                a, b, c = self.memory[self.ip + 1 : self.ip + 4]
                a = self.param_value(instruction.modes[0], a)
                b = self.param_value(instruction.modes[1], b)
                if instruction.modes[2] == 2:
                    c = self.relative_base + c
                self.memory[c] = int(a == b)
                self.ip += 4
            elif instruction.opcode == Opcode.RELATIVE_BASE:
                a = self.memory[self.ip + 1]
                a = self.param_value(instruction.modes[0], a)
                self.relative_base += a
                self.ip += 2
            else:
                raise IntcodeException(f"Unhandled instruction {instruction}")

            instruction = Instruction(self.memory[self.ip])
