from __future__ import annotations
import os
import re
import math
import itertools
from dataclasses import dataclass
from typing import List


@dataclass
class Vec:

    x: int = 0
    y: int = 0
    z: int = 0

    def __add__(self, vec: Vec) -> Vec:
        return Vec(self.x + vec.x, self.y + vec.y, self.z + vec.z)


@dataclass
class Moon:

    pos: Vec
    vel: Vec  # TODO: Use field / factorymethod to set this by default
    name: str

    def update(self) -> None:
        self.pos = self.pos + self.vel

    @property
    def total_energy(self) -> int:
        return (abs(self.pos.x) + abs(self.pos.y) + abs(self.pos.z)) * (
            abs(self.vel.x) + abs(self.vel.y) + abs(self.vel.z)
        )


def lcm(x, y, z) -> int:

    a = x * y // math.gcd(x, y)
    b = a * z // math.gcd(a, z)
    return b


if __name__ == "__main__":

    with open(os.path.join("inputs", "day12.in")) as f:
        lines = f.readlines()

    pattern = r"<x=([0-9-]+), y=([0-9-]+), z=([0-9-]+)>"
    moons: List[Moon] = []
    names = ["Io", "Europa", "Ganymede", "Callisto"]
    for line in lines:
        match = re.match(pattern, line)
        if match:
            moon = Moon(
                Vec(*[int(coord) for coord in match.groups()]),
                Vec(0, 0, 0),
                names.pop(),
            )
            moons.append(moon)
        else:
            raise Exception(f"Unable to parse {line}")

    pairs = list(itertools.combinations(moons, 2))
    for step in range(1000):

        # Compute gravity for each pair
        for moon_a, moon_b in pairs:

            if moon_a.pos.x < moon_b.pos.x:
                moon_a.vel.x += 1
                moon_b.vel.x -= 1
            elif moon_a.pos.x > moon_b.pos.x:
                moon_a.vel.x -= 1
                moon_b.vel.x += 1

            if moon_a.pos.y < moon_b.pos.y:
                moon_a.vel.y += 1
                moon_b.vel.y -= 1
            elif moon_a.pos.y > moon_b.pos.y:
                moon_a.vel.y -= 1
                moon_b.vel.y += 1

            if moon_a.pos.z < moon_b.pos.z:
                moon_a.vel.z += 1
                moon_b.vel.z -= 1
            elif moon_a.pos.z > moon_b.pos.z:
                moon_a.vel.z -= 1
                moon_b.vel.z += 1

        # Apply velocity to each moon
        for moon in moons:
            moon.update()

    total_energy = sum(moon.total_energy for moon in moons)
    assert total_energy == 5517

    pattern = r"<x=([0-9-]+), y=([0-9-]+), z=([0-9-]+)>"
    moons = []
    names = ["Io", "Europa", "Ganymede", "Callisto"]
    for line in lines:
        match = re.match(pattern, line)
        if match:
            moon = Moon(
                Vec(*[int(coord) for coord in match.groups()]),
                Vec(0, 0, 0),
                names.pop(),
            )
            moons.append(moon)
        else:
            raise Exception(f"Unable to parse {line}")

    states = {"x": set(), "y": set(), "z": set()}
    x_repeated = -1
    y_repeated = -1
    z_repeated = -1

    pairs = list(itertools.combinations(moons, 2))
    step = 0
    while True:

        x_state = tuple(str(moon.pos.x) + str(moon.vel.x) for moon in moons)
        if x_state in states["x"]:
            if x_repeated == -1:
                x_repeated = step
        states["x"].add(x_state)

        y_state = tuple(str(moon.pos.y) + str(moon.vel.y) for moon in moons)
        if y_state in states["y"]:
            if y_repeated == -1:
                y_repeated = step
        states["y"].add(y_state)

        z_state = tuple(str(moon.pos.z) + str(moon.vel.z) for moon in moons)
        if z_state in states["z"]:
            if z_repeated == -1:
                z_repeated = step

        if z_repeated > -1 and y_repeated > -1 and x_repeated > -1:
            break

        states["z"].add(z_state)

        # Compute gravity for each pair
        for moon_a, moon_b in pairs:

            if moon_a.pos.x < moon_b.pos.x:
                moon_a.vel.x += 1
                moon_b.vel.x -= 1
            elif moon_a.pos.x > moon_b.pos.x:
                moon_a.vel.x -= 1
                moon_b.vel.x += 1

            if moon_a.pos.y < moon_b.pos.y:
                moon_a.vel.y += 1
                moon_b.vel.y -= 1
            elif moon_a.pos.y > moon_b.pos.y:
                moon_a.vel.y -= 1
                moon_b.vel.y += 1

            if moon_a.pos.z < moon_b.pos.z:
                moon_a.vel.z += 1
                moon_b.vel.z -= 1
            elif moon_a.pos.z > moon_b.pos.z:
                moon_a.vel.z -= 1
                moon_b.vel.z += 1

        # Apply velocity to each moon
        for moon in moons:
            moon.update()

        step += 1

    lcm_res = lcm(x_repeated, y_repeated, z_repeated)
    assert lcm_res == 303_070_460_651_184
