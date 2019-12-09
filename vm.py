from dataclasses import dataclass, field
from typing import List, ClassVar
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


class Mode(Enum):

    POSITION = 0
    IMMEDIATE = 1
    RELATIVE = 2


@dataclass
class Instruction:

    instruction: int
    opcode: Opcode = field(init=False)
    modes: List[Mode] = field(init=False)

    def __post_init__(self) -> None:
        self.opcode = Opcode(self.instruction % 100)
        self.modes = [
            Mode(self.instruction // 100 % 10),
            Mode(self.instruction // 1000 % 10),
            Mode(self.instruction // 10000 % 10),
        ]


@dataclass
class Machine:

    memory: List[int]
    inputs: List[int]
    ip: int = 0
    output: List[int] = field(default_factory=list)
    pause_on_output: bool = False
    relative_base: int = 0

    MEMORY_SIZE: ClassVar[int] = 4096

    def __post_init__(self) -> None:
        self.memory = self.memory[:] + [0] * (Machine.MEMORY_SIZE - len(self.memory))

    @property
    def halted(self) -> bool:
        return Instruction(self.memory[self.ip]).opcode == Opcode.HALT

    def apply_mode(self, mode: Mode, param: int) -> int:
        if mode == Mode.POSITION:
            return self.memory[param]
        elif mode == Mode.IMMEDIATE:
            return param
        elif mode == Mode.RELATIVE:
            return self.memory[self.relative_base + param]
        else:
            raise IntcodeException(f"Unknown mode {mode}")

    def execute(self) -> None:

        instruction = Instruction(self.memory[self.ip])

        while instruction.opcode != Opcode.HALT:

            if instruction.opcode == Opcode.ADD:
                a, b, c = self.memory[self.ip + 1 : self.ip + 4]
                a = self.apply_mode(instruction.modes[0], a)
                b = self.apply_mode(instruction.modes[1], b)
                if instruction.modes[2] == Mode.RELATIVE:
                    c = self.relative_base + c
                self.memory[c] = a + b
                self.ip += 4
            elif instruction.opcode == Opcode.MULTIPLY:
                a, b, c = self.memory[self.ip + 1 : self.ip + 4]
                a = self.apply_mode(instruction.modes[0], a)
                b = self.apply_mode(instruction.modes[1], b)
                if instruction.modes[2] == Mode.RELATIVE:
                    c = self.relative_base + c
                self.memory[c] = a * b
                self.ip += 4
            elif instruction.opcode == Opcode.SAVE:
                a = self.memory[self.ip + 1]
                if instruction.modes[0] == Mode.RELATIVE:
                    a = self.relative_base + a
                self.memory[a] = self.inputs[0]
                self.inputs = self.inputs[1:]
                self.ip += 2
            elif instruction.opcode == Opcode.PRINT:
                a = self.memory[self.ip + 1]
                msg = self.apply_mode(instruction.modes[0], a)
                self.output.append(msg)
                self.ip += 2
                if self.pause_on_output:
                    return
            elif instruction.opcode == Opcode.JUMP_IF_TRUE:
                a, b = self.memory[self.ip + 1 : self.ip + 3]
                a = self.apply_mode(instruction.modes[0], a)
                b = self.apply_mode(instruction.modes[1], b)
                self.ip = b if a != 0 else self.ip + 3
            elif instruction.opcode == Opcode.JUMP_IF_FALSE:
                a, b = self.memory[self.ip + 1 : self.ip + 3]
                a = self.apply_mode(instruction.modes[0], a)
                b = self.apply_mode(instruction.modes[1], b)
                self.ip = b if a == 0 else self.ip + 3
            elif instruction.opcode == Opcode.LESS_THAN:
                a, b, c = self.memory[self.ip + 1 : self.ip + 4]
                a = self.apply_mode(instruction.modes[0], a)
                b = self.apply_mode(instruction.modes[1], b)
                if instruction.modes[2] == Mode.RELATIVE:
                    c = self.relative_base + c
                self.memory[c] = int(a < b)
                self.ip += 4
            elif instruction.opcode == Opcode.EQUALS:
                a, b, c = self.memory[self.ip + 1 : self.ip + 4]
                a = self.apply_mode(instruction.modes[0], a)
                b = self.apply_mode(instruction.modes[1], b)
                if instruction.modes[2] == Mode.RELATIVE:
                    c = self.relative_base + c
                self.memory[c] = int(a == b)
                self.ip += 4
            elif instruction.opcode == Opcode.RELATIVE_BASE:
                a = self.memory[self.ip + 1]
                a = self.apply_mode(instruction.modes[0], a)
                self.relative_base += a
                self.ip += 2
            else:
                raise IntcodeException(f"Unhandled instruction {instruction}")

            instruction = Instruction(self.memory[self.ip])
