import os
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
        return

    for sub_chemical, sub_quantity in reactions[chemical]["requires"]:

        # TODO: This completely kills the performance... The second part
        # will probably be impossible to do like this... You need to
        # take in the multiplier for this somehow
        while (produced[sub_chemical] - consumed[sub_chemical]) < sub_quantity:
            produce(sub_chemical, sub_quantity, reactions)

        consumed[sub_chemical] += sub_quantity

    produced[chemical] += reactions[chemical]["quantity"]


if __name__ == "__main__":

    with open(os.path.join("inputs", "day14.in")) as f:
        raw = [line.strip() for line in f.readlines()]

    # First part
    reactions = parse_reactions(raw)
    produce("FUEL", 1, reactions)
    assert produced["ORE"] == 220019

    # First part assertion
    produced.clear()
    consumed.clear()
    raw = [
        "157 ORE => 5 NZVS",
        "165 ORE => 6 DCFZ",
        "44 XJWVT, 5 KHKGT, 1 QDVJ, 29 NZVS, 9 GPVTF, 48 HKGWZ => 1 FUEL",
        "12 HKGWZ, 1 GPVTF, 8 PSHF => 9 QDVJ",
        "179 ORE => 7 PSHF",
        "177 ORE => 5 HKGWZ",
        "7 DCFZ, 7 PSHF => 2 XJWVT",
        "165 ORE => 2 GPVTF",
        "3 DCFZ, 7 NZVS, 5 HKGWZ, 10 PSHF => 8 KHKGT",
    ]
    reactions = parse_reactions(raw)
    produce("FUEL", 1, reactions)
    assert produced["ORE"] == 13312

    # First part assertion
    produced.clear()
    consumed.clear()
    raw = [
        "2 VPVL, 7 FWMGM, 2 CXFTF, 11 MNCFX => 1 STKFG",
        "17 NVRVD, 3 JNWZP => 8 VPVL",
        "53 STKFG, 6 MNCFX, 46 VJHF, 81 HVMC, 68 CXFTF, 25 GNMV => 1 FUEL",
        "22 VJHF, 37 MNCFX => 5 FWMGM",
        "139 ORE => 4 NVRVD",
        "144 ORE => 7 JNWZP",
        "5 MNCFX, 7 RFSQX, 2 FWMGM, 2 VPVL, 19 CXFTF => 3 HVMC",
        "5 VJHF, 7 MNCFX, 9 VPVL, 37 CXFTF => 6 GNMV",
        "145 ORE => 6 MNCFX",
        "1 NVRVD => 8 CXFTF",
        "1 VJHF, 6 MNCFX => 4 RFSQX",
        "176 ORE => 6 VJHF",
    ]
    reactions = parse_reactions(raw)
    produce("FUEL", 1, reactions)
    assert produced["ORE"] == 180697

    # First part example
    produced.clear()
    consumed.clear()
    raw = [
        "171 ORE => 8 CNZTR",
        "7 ZLQW, 3 BMBT, 9 XCVML, 26 XMNCP, 1 WPTQ, 2 MZWV, 1 RJRHP => 4 PLWSL",
        "114 ORE => 4 BHXH",
        "14 VRPVC => 6 BMBT",
        "6 BHXH, 18 KTJDG, 12 WPTQ, 7 PLWSL, 31 FHTLT, 37 ZDVW => 1 FUEL",
        "6 WPTQ, 2 BMBT, 8 ZLQW, 18 KTJDG, 1 XMNCP, 6 MZWV, 1 RJRHP => 6 FHTLT",
        "15 XDBXC, 2 LTCX, 1 VRPVC => 6 ZLQW",
        "13 WPTQ, 10 LTCX, 3 RJRHP, 14 XMNCP, 2 MZWV, 1 ZLQW => 1 ZDVW",
        "5 BMBT => 4 WPTQ",
        "189 ORE => 9 KTJDG",
        "1 MZWV, 17 XDBXC, 3 XCVML => 2 XMNCP",
        "12 VRPVC, 27 CNZTR => 2 XDBXC",
        "15 KTJDG, 12 BHXH => 5 XCVML",
        "3 BHXH, 2 VRPVC => 7 MZWV",
        "121 ORE => 7 VRPVC",
        "7 XCVML => 6 RJRHP",
        "5 BHXH, 4 VRPVC => 5 LTCX",
    ]

    reactions = parse_reactions(raw)
    produce("FUEL", 1, reactions)
    assert produced["ORE"] == 2210736
