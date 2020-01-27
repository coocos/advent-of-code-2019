from __future__ import annotations
import os
import re
import math
import itertools
from dataclasses import dataclass
from typing import List, Tuple, Set, Dict


@dataclass
class Vec:

    x: int = 0
    y: int = 0
    z: int = 0

    def __add__(self, vec: Vec) -> Vec:
        return Vec(self.x + vec.x, self.y + vec.y, self.z + vec.z)

    def __getitem__(self, key: str) -> int:
        assert key in "xyz"
        return getattr(self, key)

    def __setitem__(self, key: str, value: int) -> None:
        assert key in "xyz"
        setattr(self, key, value)


@dataclass
class Moon:

    pos: Vec
    vel: Vec

    def update(self) -> None:
        self.pos = self.pos + self.vel

    @property
    def total_energy(self) -> int:
        return (abs(self.pos.x) + abs(self.pos.y) + abs(self.pos.z)) * (
            abs(self.vel.x) + abs(self.vel.y) + abs(self.vel.z)
        )


def lcm(x: int, y: int, z: int) -> int:

    a = x * y // math.gcd(x, y)
    b = a * z // math.gcd(a, z)
    return b


def parse_moons(input_list: List[str]) -> List[Moon]:

    pattern = r"<x=([0-9-]+), y=([0-9-]+), z=([0-9-]+)>"
    moons: List[Moon] = []
    for line in input_list:
        match = re.match(pattern, line)
        if match:
            moon = Moon(Vec(*[int(coord) for coord in match.groups()]), Vec(0, 0, 0),)
            moons.append(moon)
        else:
            raise Exception(f"Unable to parse {line}")
    return moons


if __name__ == "__main__":

    with open(os.path.join("inputs", "day12.in")) as f:
        lines = f.readlines()

    # First part
    moons = parse_moons(lines)
    pairs = list(itertools.combinations(moons, 2))
    for step in range(1000):

        # Compute gravity for each pair
        for moon_a, moon_b in pairs:

            for c in "xyz":
                if moon_a.pos[c] < moon_b.pos[c]:
                    moon_a.vel[c] += 1
                    moon_b.vel[c] -= 1
                elif moon_a.pos[c] > moon_b.pos[c]:
                    moon_a.vel[c] -= 1
                    moon_b.vel[c] += 1

        # Apply velocity to each moon
        for moon in moons:
            moon.update()

    total_energy = sum(moon.total_energy for moon in moons)
    assert total_energy == 5517

    # Second part - each axis is independent so find the cycle independently
    # for each axis and then compute the lowest common multiple of the cycles
    moons = parse_moons(lines)

    states: Dict[str, Set[Tuple[str, ...]]] = {"x": set(), "y": set(), "z": set()}
    repeated = {"x": -1, "y": -1, "z": -1}

    pairs = list(itertools.combinations(moons, 2))
    step = 0
    while True:

        # Keep track of state for each axis
        for c in "xyz":
            state = tuple(
                str(getattr(moon.pos, c)) + str(getattr(moon.vel, c)) for moon in moons
            )
            if state in states[c]:
                if repeated[c] == -1:
                    repeated[c] = step
            states[c].add(state)

        # Cycles found for each xis
        if all(step > -1 for step in repeated.values()):
            break

        # Compute gravity for each pair
        for moon_a, moon_b in pairs:

            for c in "xyz":
                if moon_a.pos[c] < moon_b.pos[c]:
                    moon_a.vel[c] += 1
                    moon_b.vel[c] -= 1
                elif moon_a.pos[c] > moon_b.pos[c]:
                    moon_a.vel[c] -= 1
                    moon_b.vel[c] += 1

        # Apply velocity to each moon
        for moon in moons:
            moon.update()

        step += 1

    lcm_res = lcm(repeated["x"], repeated["y"], repeated["z"])
    assert lcm_res == 303_070_460_651_184
