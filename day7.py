import os
import itertools
from vm import Machine


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
