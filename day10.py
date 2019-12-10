from __future__ import annotations
import os
import math
import collections
from typing import List, Any
from dataclasses import dataclass


@dataclass
class Vector:

    x: int
    y: int

    @property
    def magnitude(self) -> int:
        return math.sqrt(self.x ** 2 + self.y ** 2)

    def direction(self) -> Vector:
        """
        if self.x == 0:
            return Vector(self.x, self.y // abs(self.y))
        elif self.y == 0:
            return Vector(self.x // abs(self.x), self.y)
        else:
            # return Vector(self.x / abs(self.x), self.y / abs(self.x))
            gcd = abs(math.gcd(self.x, self.y))
            return Vector(self.x // gcd, self.y // gcd)
        """
        gcd = abs(math.gcd(self.x, self.y))
        return Vector(self.x // gcd, self.y // gcd)


@dataclass
class Asteroid:

    pos: Vector


def parse_asteroids(grid: List[List[str]]) -> List[Asteroid]:

    asteroids = []
    for y in range(len(grid)):
        for x in range(len(grid[y])):
            if grid[y][x] == "#":
                asteroids.append(Asteroid(Vector(x, y)))

    return asteroids


def count_visible_asteroids(origin: Asteroid, asteroids: List[Asteroid]) -> int:

    visible = set()
    for asteroid in asteroids:
        if asteroid != origin:
            direction = Vector(
                asteroid.pos.x - origin.pos.x, asteroid.pos.y - origin.pos.y
            ).direction()
            visible.add((direction.x, direction.y))

    return len(visible)


def group_asteroids(station: Asteroid, asteroids: List[Asteroid]) -> Any:

    groups = collections.defaultdict(list)
    for asteroid in asteroids:
        if asteroid != station:
            from_station_to_asteroid = Vector(
                asteroid.pos.x - station.pos.x, asteroid.pos.y - station.pos.y
            )
            direction = from_station_to_asteroid.direction()
            magnitude = from_station_to_asteroid.magnitude
            groups[(direction.x, direction.y)].append((asteroid, magnitude))

    # FIXME: Ugh
    for group in groups.values():
        group.sort(key=lambda asteroid_distance: asteroid_distance[1], reverse=True)

    return groups


if __name__ == "__main__":

    # First test case
    data = """......#.#.
        #..#.#....
        ..#######.
        .#.#.###..
        .#..#.....
        ..#....#.#
        #..#....#.
        .##.#..###
        ##...#..#.
        .#....####"""
    grid = [list(line.strip()) for line in data.split("\n")]
    asteroids = parse_asteroids(grid)
    visibility = [
        (asteroid, count_visible_asteroids(asteroid, asteroids))
        for asteroid in asteroids
    ]
    asteroid, visible = max(
        visibility, key=lambda asteroid_visibility: asteroid_visibility[1]
    )
    assert asteroid.pos == Vector(5, 8)
    assert visible == 33

    # Second test case
    data = """#.#...#.#.
        .###....#.
        .#....#...
        ##.#.#.#.#
        ....#.#.#.
        .##..###.#
        ..#...##..
        ..##....##
        ......#...
        .####.###."""
    grid = [list(line.strip()) for line in data.split("\n")]
    asteroids = parse_asteroids(grid)
    visibility = [
        (asteroid, count_visible_asteroids(asteroid, asteroids))
        for asteroid in asteroids
    ]
    asteroid, visible = max(
        visibility, key=lambda asteroid_visibility: asteroid_visibility[1]
    )
    assert asteroid.pos == Vector(1, 2)
    assert visible == 35

    # Third test case
    data = """.#..#..###
        ####.###.#
        ....###.#.
        ..###.##.#
        ##.##.#.#.
        ....###..#
        ..#.#..#.#
        #..#.#.###
        .##...##.#
        .....#.#.."""
    grid = [list(line.strip()) for line in data.split("\n")]
    asteroids = parse_asteroids(grid)
    visibility = [
        (asteroid, count_visible_asteroids(asteroid, asteroids))
        for asteroid in asteroids
    ]
    asteroid, visible = max(
        visibility, key=lambda asteroid_visibility: asteroid_visibility[1]
    )
    assert asteroid.pos == Vector(6, 3)
    assert visible == 41

    # Fourth test case
    data = """.#..##.###...#######
        ##.############..##.
        .#.######.########.#
        .###.#######.####.#.
        #####.##.#.##.###.##
        ..#####..#.#########
        ####################
        #.####....###.#.#.##
        ##.#################
        #####.##.###..####..
        ..######..##.#######
        ####.##.####...##..#
        .#####..#.######.###
        ##...#.##########...
        #.##########.#######
        .####.#.###.###.#.##
        ....##.##.###..#####
        .#.#.###########.###
        #.#.#.#####.####.###
        ###.##.####.##.#..##"""

    grid = [list(line.strip()) for line in data.split("\n")]
    asteroids = parse_asteroids(grid)
    visibility = [
        (asteroid, count_visible_asteroids(asteroid, asteroids))
        for asteroid in asteroids
    ]
    asteroid, visible = max(
        visibility, key=lambda asteroid_visibility: asteroid_visibility[1]
    )
    assert asteroid.pos == Vector(11, 13)
    assert visible == 210

    # First part
    with open(os.path.join("inputs", "day10.in")) as f:
        grid = [list(line.strip()) for line in f.readlines()]

    asteroids = parse_asteroids(grid)
    visibility = [
        (asteroid, count_visible_asteroids(asteroid, asteroids))
        for asteroid in asteroids
    ]
    asteroid, visible = max(
        visibility, key=lambda asteroid_visibility: asteroid_visibility[1]
    )
    assert asteroid.pos == Vector(29, 28)
    assert visible == 256

    # Second part
    data = """.#..##.###...#######
        ##.############..##.
        .#.######.########.#
        .###.#######.####.#.
        #####.##.#.##.###.##
        ..#####..#.#########
        ####################
        #.####....###.#.#.##
        ##.#################
        #####.##.###..####..
        ..######..##.#######
        ####.##.####...##..#
        .#####..#.######.###
        ##...#.##########...
        #.##########.#######
        .####.#.###.###.#.##
        ....##.##.###..#####
        .#.#.###########.###
        #.#.#.#####.####.###
        ###.##.####.##.#..##"""

    grid = [list(line.strip()) for line in data.split("\n")]

    # First part
    with open(os.path.join("inputs", "day10.in")) as f:
        grid = [list(line.strip()) for line in f.readlines()]

    asteroids = parse_asteroids(grid)
    visibility = [
        (asteroid, count_visible_asteroids(asteroid, asteroids))
        for asteroid in asteroids
    ]
    station, visible = max(
        visibility, key=lambda asteroid_visibility: asteroid_visibility[1]
    )

    # assert station.pos == Vector(11, 13)
    # assert visible == 210

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

    quadrants["tr"].sort(key=lambda d: math.atan2(-d[1], d[0]), reverse=True)
    quadrants["br"].sort(key=lambda d: math.atan2(d[1], d[0]))
    quadrants["bl"].sort(key=lambda d: math.atan2(d[1], -d[0]), reverse=True)
    quadrants["tl"].sort(key=lambda d: math.atan2(-d[1], d[0]), reverse=True)
    asteroid_groups = (
        quadrants["tr"] + quadrants["br"] + quadrants["bl"] + quadrants["tl"]
    )

    vaporized: List[Asteroid] = []
    for group in asteroid_groups:
        vaporized.append(groups[group].pop())
        if len(vaporized) == 200:
            break

    assert vaporized[-1][0].pos == Vector(17, 7)
