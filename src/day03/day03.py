from collections import namedtuple
from math import prod
from typing import Dict, List, Set

Coordinates = namedtuple("Coordinates", ["x", "y"])


def parsed_input() -> List[str]:
    with open("input.dat", "r") as data:
        return [line.strip() for line in data.readlines()]


def to_coordinates_dict(matrix: List[str]) -> Dict[Coordinates, str]:
    return {
        Coordinates(x, y): cell
        for x, line in enumerate(matrix)
        for y, cell in enumerate(line)
    }


def coordinate_has_adjacent_symbols(
    coordinates_dict: Dict[Coordinates, str], coordinates: Coordinates
):
    def is_symbol(cell: str):
        return not cell.isdigit() and cell != "."

    return any(
        is_symbol(cell)
        for cell in get_adjacent_cells(coordinates_dict, coordinates).values()
    )


def get_adjacent_stars_coordinates(
    coordinates_dict: Dict[Coordinates, str], coordinates: Coordinates
) -> Set[Coordinates]:
    return {
        coordinates
        for coordinates, cell in get_adjacent_cells(
            coordinates_dict, coordinates
        ).items()
        if cell == "*"
    }


def get_adjacent_cells(
    coordinates_dict: Dict[Coordinates, str], coordinates: Coordinates
) -> Dict[Coordinates, str]:
    x, y = coordinates
    adjacents_x = x - 1, x, x + 1
    adjacents_y = y - 1, y, y + 1

    return {
        (i, j): coordinates_dict[(i, j)]
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
            if cell.isdigit() and coordinate_has_adjacent_symbols(
                coordinates_dict, (i, j)
            ):
                current_number_is_valid = True
                current_number += cell

            elif cell.isdigit():
                current_number += cell
            elif len(current_number) > 0 and current_number_is_valid:
                res += int(current_number)

                current_number = ""
                current_number_is_valid = False
            else:
                current_number = ""
                current_number_is_valid = False
    return res


def part_two(matrix: List[str]):
    coordinates_dict = to_coordinates_dict(matrix)
    numbers_adjacents_to_star_symbols: Dict[Coordinates, List[int]] = {
        k: [] for k, v in coordinates_dict.items() if v == "*"
    }

    def track_numbers_adjacents_to_star_symbols(adjacent_star_coordinates_, current_number_):
        for coordinates in adjacent_star_coordinates_:
            numbers_adjacents_to_star_symbols[coordinates].append(
                int(current_number_)
            )

    current_number = ""
    adjacent_star_coordinates = set()
    for i, line in enumerate(matrix):
        for j, cell in enumerate(line):
            adjacent_stars = get_adjacent_stars_coordinates(coordinates_dict, (i, j))
            if cell.isdigit() and len(adjacent_stars) > 0:
                adjacent_star_coordinates = adjacent_star_coordinates.union(
                    adjacent_stars
                )
                current_number += cell
            elif cell.isdigit():
                current_number += cell
            elif len(current_number) > 0 and len(adjacent_star_coordinates) > 0:
                track_numbers_adjacents_to_star_symbols(adjacent_star_coordinates, current_number)

                current_number = ""
                adjacent_star_coordinates = set()
            else:
                current_number = ""
                adjacent_star_coordinates = set()

    gear_ratios = (
        prod(numbers)
        for numbers in numbers_adjacents_to_star_symbols.values()
        if len(numbers) == 2
    )

    return sum(gear_ratios)


if __name__ == "__main__":
    print(part_one(parsed_input()), part_two(parsed_input()))
