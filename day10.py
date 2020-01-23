from __future__ import annotations
import os
import math
import collections
from operator import itemgetter
from typing import List, DefaultDict, Tuple, Set
from dataclasses import dataclass


@dataclass
class Vector:

    x: int
    y: int

    @property
    def magnitude(self) -> float:
        return math.sqrt(self.x ** 2 + self.y ** 2)

    def normalized(self) -> Vector:
        # We can't normalize the vector the normal way by dividing all
        # the components by the magnitude of the vector because we want
        # to keep things stricly in the integer realm of things so find
        # the greatest common divisor and divide components by it
        gcd = abs(math.gcd(self.x, self.y))
        return Vector(self.x // gcd, self.y // gcd)


def parse_asteroids(grid: List[List[str]]) -> List[Vector]:

    asteroids = []
    for y in range(len(grid)):
        for x in range(len(grid[y])):
            if grid[y][x] == "#":
                asteroids.append(Vector(x, y))

    return asteroids


def count_visible_asteroids(origin: Vector, asteroids: List[Vector]) -> int:

    visible: Set[Tuple[int, int]] = set()
    for asteroid in asteroids:
        if asteroid != origin:
            direction = Vector(
                asteroid.x - origin.x, asteroid.y - origin.y
            ).normalized()
            visible.add((direction.x, direction.y))

    return len(visible)


def group_asteroids(station: Vector, asteroids: List[Vector]) -> DefaultDict:

    groups: DefaultDict[
        Tuple[int, int], List[Tuple[Vector, float]]
    ] = collections.defaultdict(list)
    for asteroid in asteroids:
        if asteroid != station:
            from_station_to_asteroid = Vector(
                asteroid.x - station.x, asteroid.y - station.y
            )
            direction = from_station_to_asteroid.normalized()
            magnitude = from_station_to_asteroid.magnitude
            groups[(direction.x, direction.y)].append((asteroid, magnitude))

    # Be nasty and sort the groups by distance here
    for group in groups.values():
        group.sort(key=itemgetter(1), reverse=True)

    return groups


if __name__ == "__main__":

    # First part
    with open(os.path.join("inputs", "day10.in")) as f:
        grid = [list(line.strip()) for line in f.readlines()]

    asteroids = parse_asteroids(grid)
    visibility = [
        (asteroid, count_visible_asteroids(asteroid, asteroids))
        for asteroid in asteroids
    ]
    station, visible = max(visibility, key=itemgetter(1))
    assert station == Vector(29, 28)
    assert visible == 256

    # Second part
    groups = group_asteroids(station, asteroids)

    quadrants = {"tr": [], "br": [], "bl": [], "tl": []}
    for direction in groups:
        if direction[0] >= 0:
            if direction[1] < 0:
                quadrants["tr"].append(direction)
            else:
                quadrants["br"].append(direction)
        else:
            if direction[1] < 0:
                quadrants["tl"].append(direction)
            else:
                quadrants["bl"].append(direction)

    # Oh dear
    quadrants["tr"].sort(key=lambda d: math.atan2(-d[1], d[0]), reverse=True)
    quadrants["br"].sort(key=lambda d: math.atan2(d[1], d[0]))
    quadrants["bl"].sort(key=lambda d: math.atan2(d[1], -d[0]), reverse=True)
    quadrants["tl"].sort(key=lambda d: math.atan2(-d[1], d[0]), reverse=True)

    asteroid_groups = (
        quadrants["tr"] + quadrants["br"] + quadrants["bl"] + quadrants["tl"]
    )

    vaporized: List[Vector] = []
    for group in asteroid_groups:
        asteroid, _ = groups[group].pop()
        vaporized.append(asteroid)
        if len(vaporized) == 200:
            break

    assert vaporized[199] == Vector(17, 7)
