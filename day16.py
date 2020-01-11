import os
import collections
from typing import List


def fft(signal: str, phases: int = 1) -> str:

    base_pattern = [0, 1, 0, -1]

    # Generate the patterns
    patterns = []
    for position in range(1, len(signal) + 1):
        partial_pattern: List[int] = []
        for multiplier in base_pattern:
            partial_pattern += [multiplier] * position
        patterns.append(collections.deque(partial_pattern))

    phased = [int(s) for s in signal]

    # Apply the phases
    for _ in range(phases):

        next_phase = []
        for i in range(len(phased)):
            pattern = patterns[i].copy()
            pattern.rotate(-1)

            signal_sum = 0
            for s in phased:
                signal_sum += s * pattern[0]
                pattern.rotate(-1)
            next_phase.append(abs(signal_sum) % 10)

        phased = next_phase

    return "".join(str(s) for s in phased)


if __name__ == "__main__":

    with open(os.path.join("inputs", "day16.in")) as f:
        signal = f.read().strip()

    assert fft(signal, 100)[:8] == "17978331"
