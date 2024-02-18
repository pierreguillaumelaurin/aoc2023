from typing import List

from src.coordinates import to_coordinates_dict
from src.utils import benchmark


def parsed_input():
    with open("./input.dat", "r") as data:
        return [line.strip() for line in data.readlines()]


entrances = {
    "|": {(1,0), (-1,0)},
    "-": ("-"),
    "L": (),
    "J": (),
    "7": (),
    "F": (),
    "S": (),
}


@benchmark
def part_one(matrix: List[str]):
    coordinates_dict = to_coordinates_dict(matrix)
