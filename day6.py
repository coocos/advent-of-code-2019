from __future__ import annotations
import os
import sys
from dataclasses import dataclass, field
from typing import List, Dict


# Let's go berserk
sys.setrecursionlimit(2048)


@dataclass
class OrbitObject:

    name: str
    children: List[OrbitObject] = field(default_factory=list)
    orbits: int = 0


OrbitMap = Dict[str, OrbitObject]


def map_orbits(orbits: List[List[str]]) -> OrbitMap:

    orbit_map: OrbitMap = {}
    for target, orbiter in orbits:
        if target not in orbit_map:
            orbit_map[target] = OrbitObject(target)
        if orbiter not in orbit_map:
            orbit_map[orbiter] = OrbitObject(orbiter)
        orbit_map[target].children.append(orbit_map[orbiter])

    return orbit_map


def orbit_checksum(orbiter: OrbitObject, depth: int = 0) -> int:

    if not orbiter:
        return 0

    # Mutating the orbiter here is nasty but oh well
    orbiter.orbits = depth

    return depth + sum(orbit_checksum(child, depth + 1) for child in orbiter.children)


def path_to(target: str, current: OrbitObject) -> List[OrbitObject]:

    if not current:
        return []

    if current.name == target:
        return [current]

    for child in current.children:
        path = path_to(target, child)
        if path:
            return [current] + path

    return []


def lowest_common_ancestor(root: OrbitObject, first: str, second: str) -> OrbitObject:

    path_to_first = path_to(first, root)
    path_to_second = path_to(second, root)
    ancestors = set([node.name for node in path_to_first])
    for ancestor in reversed(path_to_second):
        if ancestor.name in ancestors:
            return ancestor

    raise Exception("No common ancestors found")


if __name__ == "__main__":

    with open(os.path.join("inputs", "day6.in")) as f:
        orbits = [line.strip().split(")") for line in f.readlines()]

    orbit_map = map_orbits(orbits)
    checksum = orbit_checksum(orbit_map["COM"])
    assert checksum == 314247

    ancestor = lowest_common_ancestor(orbit_map["COM"], "YOU", "SAN")
    san_to_ancestor = orbit_map["SAN"].orbits - ancestor.orbits - 1
    you_to_ancestor = orbit_map["YOU"].orbits - ancestor.orbits - 1
    assert san_to_ancestor + you_to_ancestor == 514
