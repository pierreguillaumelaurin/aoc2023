from collections import namedtuple
from typing import Dict, Tuple, List, Optional, Type, Set

INVALID_CHARS = ["."]

Coordinates = namedtuple("Coordinates", ["x", "y"])


def parsed_input() -> List[List[str]]:
    with open("input.dat", "r") as data:
        return [list(line.strip()) for line in data.readlines()]


def is_symbol(cell: str):
    return not cell.isdigit() and cell not in INVALID_CHARS


def to_coordinates_dict(matrix: List[str]) -> Dict[Coordinates, str]:
    return {
        Coordinates(x, y): cell
        for x, line in enumerate(matrix)
        for y, cell in enumerate(line)
    }


def coordinate_has_adjacent_symbols(coordinates_dict: Dict[Coordinates, str], coordinates: Coordinates):
    return any(
        is_symbol(cell)
        for cell in get_adjacent_cells(coordinates_dict, coordinates).values()
    )


def get_adjacent_cells(coordinates_dict: Dict[Coordinates, str], coordinates: Coordinates) -> Dict[Coordinates, str]:
    x, y = coordinates
    adjacents_x = x - 1, x, x + 1
    adjacents_y = y - 1, y, y + 1

    return {
        (i,j): coordinates_dict[(i,j)]
        for i in adjacents_x
        for j in adjacents_y
        if (i, j) in coordinates_dict.keys()
    }


def part_one(matrix: List[str]):
    coordinates_dict = to_coordinates_dict(matrix)
    res = 0
    current_number = ""
    current_number_is_valid = False
    for i, line in enumerate(matrix):
        for j, cell in enumerate(line):
            if cell.isdigit() and coordinate_has_adjacent_symbols(coordinates_dict, (i, j)):
                current_number_is_valid = True

            if cell.isdigit():
                current_number += cell
            elif len(current_number) > 0 and current_number_is_valid:
                res += int(current_number)
                current_number = ""
                current_number_is_valid = False
            else:
                current_number = ""
                current_number_is_valid = False
    return res


def part_two(input_):
    pass


if __name__ == "__main__":
    print(part_one(parsed_input()), part_two(parsed_input()))
    assert part_one(parsed_input()) == 535235
