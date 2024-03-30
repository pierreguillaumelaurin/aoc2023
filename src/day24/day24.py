from typing import TypedDict, Tuple, List

from src.utils import benchmark


class Hailstone(TypedDict):
    position: Tuple[int, int, int]
    velocity: Tuple[int, int, int]


def parsed_input():
    with open("./input.dat", "r") as data:
        _parsed_input = []

        for line in data.readlines():
            position, velocity = line.strip().split(' @ ')
            _parsed_input.append({'position': position.split(', '), 'velocity': velocity.split(', ')})

        return _parsed_input


@benchmark
def part_one(hailstones: List[Hailstone], lower_bound=200000000000000, higher_bound=400000000000000):
    return hailstones


if __name__ == "__main__":
    print(part_one(parsed_input()))
