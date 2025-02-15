import os


def fuel_required(mass: int) -> int:

    return mass // 3 - 2


def total_fuel_required(fuel: int) -> int:

    if fuel <= 0:
        return 0

    needed_fuel = fuel_required(fuel)
    return fuel + total_fuel_required(needed_fuel)


if __name__ == "__main__":

    with open(os.path.join("inputs", "day1.in")) as f:
        module_masses = [int(line) for line in f.readlines()]

    # First part
    assert sum(fuel_required(m) for m in module_masses) == 3382136

    # Second part
    assert sum(total_fuel_required(fuel_required(m)) for m in module_masses) == 5070314
