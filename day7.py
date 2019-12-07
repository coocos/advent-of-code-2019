import os
import itertools
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
    HALT = 99


class Instruction:
    def __init__(self, instruction: int):
        self.instruction = instruction
        self.opcode = Opcode(instruction % 100)

        # FIXME: Ugh
        modes = str(instruction)[:-2]
        modes = "0" * (3 - len(modes)) + modes
        self.modes = [int(mode) for mode in reversed(modes)]

    def __repr__(self):
        return (
            f"Instruction: {self.instruction} Opcode: {self.opcode} Modes: {self.modes}"
        )


@dataclass
class Machine:

    program: List[int]
    inputs: List[int]
    ip: int = 0
    input_pointer: int = 0
    output: List[int] = field(default_factory=list)
    pause_on_output: bool = False

    @property
    def halted(self):
        return Instruction(self.program[self.ip]).opcode == Opcode.HALT

    def execute(self):

        instruction = Instruction(self.program[self.ip])

        while instruction.opcode != Opcode.HALT:

            if instruction.opcode == Opcode.ADD:
                a, b, c = self.program[self.ip + 1 : self.ip + 4]
                a = a if instruction.modes[0] else self.program[a]
                b = b if instruction.modes[1] else self.program[b]
                self.program[c] = a + b
                self.ip += 4
            elif instruction.opcode == Opcode.MULTIPLY:
                a, b, c = self.program[self.ip + 1 : self.ip + 4]
                a = a if instruction.modes[0] else self.program[a]
                b = b if instruction.modes[1] else self.program[b]
                self.program[c] = a * b
                self.ip += 4
            elif instruction.opcode == Opcode.SAVE:
                a = self.program[self.ip + 1]
                self.program[a] = self.inputs[self.input_pointer]
                self.input_pointer += 1
                self.ip += 2
            elif instruction.opcode == Opcode.PRINT:
                a = self.program[self.ip + 1]
                msg = a if instruction.modes[0] else self.program[a]
                self.output.append(msg)
                self.ip += 2
                if self.pause_on_output:
                    return
            elif instruction.opcode == Opcode.JUMP_IF_TRUE:
                a, b = self.program[self.ip + 1 : self.ip + 3]
                a = a if instruction.modes[0] else self.program[a]
                b = b if instruction.modes[1] else self.program[b]
                if a != 0:
                    self.ip = b
                else:
                    self.ip += 3
            elif instruction.opcode == Opcode.JUMP_IF_FALSE:
                a, b = self.program[self.ip + 1 : self.ip + 3]
                a = a if instruction.modes[0] else self.program[a]
                b = b if instruction.modes[1] else self.program[b]
                if a == 0:
                    self.ip = b
                else:
                    self.ip += 3
            elif instruction.opcode == Opcode.LESS_THAN:
                a, b, c = self.program[self.ip + 1 : self.ip + 4]
                a = a if instruction.modes[0] else self.program[a]
                b = b if instruction.modes[1] else self.program[b]
                if a < b:
                    self.program[c] = 1
                else:
                    self.program[c] = 0
                self.ip += 4
            elif instruction.opcode == Opcode.EQUALS:
                a, b, c = program[self.ip + 1 : self.ip + 4]
                a = a if instruction.modes[0] else self.program[a]
                b = b if instruction.modes[1] else self.program[b]
                if a == b:
                    self.program[c] = 1
                else:
                    self.program[c] = 0
                self.ip += 4
            else:
                raise IntcodeException(f"Unhandled instruction {instruction}")

            instruction = Instruction(program[self.ip])


if __name__ == "__main__":

    with open(os.path.join("inputs", "day7.in")) as f:
        program = [int(opcode) for opcode in f.read().strip().split(",")]

    # First part
    thruster_signals = []
    for sequence in itertools.permutations(range(5)):
        amplifier_input = 0
        for setting in sequence:
            amplifier = Machine(program[:], [setting, amplifier_input])
            amplifier.execute()
            amplifier_input = amplifier.output[0]
        thruster_signals.append(amplifier_input)
    max_thrusters = max(thruster_signals)
    assert max_thrusters == 20413

    # Second part
    thruster_signals = []
    for sequence in itertools.permutations(range(5, 10)):

        amps = [
            Machine(program[:], [setting], pause_on_output=True) for setting in sequence
        ]

        # Kickstart the first amplifier with zero signal
        amps[0].inputs.append(0)

        # The feedback loop halts when the last amplifier halts
        while not amps[-1].halted:

            for amp_no, amp in enumerate(amps):

                amp.execute()
                output_signal = amp.output[-1]
                amps[(amp_no + 1) % len(amps)].inputs.append(output_signal)

        thruster_signals.append(amps[-1].output[-1])

    assert max(thruster_signals) == 3321777
