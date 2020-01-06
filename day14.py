import os
import math
import collections
from typing import List, Dict


# Ooh nasty globals
produced = collections.defaultdict(int)
consumed = collections.defaultdict(int)


def parse_reactions(raw_reactions: List[str]) -> Dict:

    reactions = {}

    for reaction in raw_reactions:

        needed, produced = reaction.split(" => ")
        quantity, product = produced.split(" ")
        reactions[product] = {"quantity": int(quantity), "requires": []}

        for chemical_amount in needed.split(", "):
            amount, chemical = chemical_amount.split(" ")
            reactions[product]["requires"].append((chemical, int(amount)))

    return reactions


def produce(chemical: str, quantity: int, reactions: Dict) -> None:

    # We already have enough of this chemical so just consume it
    if produced[chemical] - consumed[chemical] >= quantity:
        consumed[chemical] += quantity
        return

    # If ore is needed then we can just mine it instantly
    if chemical == "ORE":
        produced[chemical] += quantity
        consumed[chemical] += quantity
        return

    already_produced = produced[chemical] - consumed[chemical]
    multiplier = math.ceil(
        (quantity - already_produced) / reactions[chemical]["quantity"]
    )

    for sub_chemical, sub_quantity in reactions[chemical]["requires"]:

        produce(sub_chemical, sub_quantity * multiplier, reactions)

    produced[chemical] += reactions[chemical]["quantity"] * multiplier
    consumed[chemical] += quantity


if __name__ == "__main__":

    with open(os.path.join("inputs", "day14.in")) as f:
        raw = [line.strip() for line in f.readlines()]

    # First part
    consumed.clear()
    produced.clear()
    reactions = parse_reactions(raw)
    produce("FUEL", 1, reactions)
    assert produced["ORE"] == 220019

    # Second part - use binary search
    trillion = 1_000_000_000_000
    high = trillion
    low = 0
    mid = high // 2
    while high >= low:
        produced.clear()
        consumed.clear()
        mid = low + (high - low) // 2
        produce("FUEL", mid, reactions)
        if consumed["ORE"] > trillion:
            high = mid - 1
        elif consumed["ORE"] < trillion:
            low = mid + 1
        else:
            break

    assert mid - 1 == 5650230
