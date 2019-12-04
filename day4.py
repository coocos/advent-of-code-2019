from collections import Counter
from typing import List


if __name__ == "__main__":

    with open("day4.in") as f:
        low, high = [int(num) for num in f.read().strip().split("-")]

    # First part
    passwords: List[str] = []
    for d in range(low, high + 1):
        digit = str(d)

        if len(set(digit)) < 6 and sorted(digit) == list(digit):
            passwords.append(digit)

    assert len(passwords) == 910

    # Second part
    stricter_passwords = [p for p in passwords if 2 in Counter(p).values()]

    assert len(stricter_passwords) == 598
