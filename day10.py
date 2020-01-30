from __future__ import annotations
import os
import math
import collections
from operator import itemgetter
from typing import List, DefaultDict, Tuple, Set, Dict
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


def dot(vec1: Tuple[float, float], vec2: Tuple[float, float]) -> float:
    return vec1[0] * vec2[0] + vec1[1] * vec2[1]


def angle(vec: Tuple[float, float]) -> Tuple[float, float]:
    norm = math.sqrt(vec[0] ** 2 + vec[1] ** 2)
    return (vec[0] / norm, vec[1] / norm)


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

    with open(os.path.join("inputs", "day10.in")) as f:
        grid = [list(line.strip()) for line in f.readlines()]

    # First part
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

    # Divide asteroid groups into 4 quadrants based on their direction from the station
    quadrants: Dict[str, List] = {"tr": [], "br": [], "bl": [], "tl": []}
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

    # Sort asteroids in each quadrant based on dot product / angle with each axis vector
    quadrants["tr"].sort(key=lambda d: dot(angle(d), (0, -1)))
    quadrants["br"].sort(key=lambda d: dot(angle(d), (1, 0)))
    quadrants["bl"].sort(key=lambda d: dot(angle(d), (0, 1)))
    quadrants["tl"].sort(key=lambda d: dot(angle(d), (1, 0)))

    # Combine quadrants to form a list of asteroid groups in a circular order
    asteroid_groups = (
        quadrants["tr"] + quadrants["br"] + quadrants["bl"] + quadrants["tl"]
    )

    # Blast away at the sorted asteroids until 200 have been vaporized
    vaporized: List[Vector] = []
    for group in asteroid_groups:
        asteroid, _ = groups[group].pop()
        vaporized.append(asteroid)
        if len(vaporized) == 200:
            break

    assert vaporized[199] == Vector(17, 7)
