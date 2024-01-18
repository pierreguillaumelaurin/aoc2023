from collections import namedtuple
from typing import Dict, Tuple, List, Optional, Type

INVALID_CHARS = [".", "\n"]

Coordinates = namedtuple("Coordinates", ["x", "y"])


def parsed_input() -> List[List[str]]:
    with open("input.dat", "r") as data:
        return [list(line.strip()) for line in data.readlines()]


def to_coordinate_dict(matrix: List[List[str]]) -> Dict[Coordinates, str]:
    return {
        Coordinates(x, y): cell
        for x, line in enumerate(matrix)
        for y, cell in enumerate(line)
    }


def part_one(input_):
    coordinate_dict = to_coordinate_dict(input_)

    def get_full_number(
        acc: Dict[Coordinates, str], coordinates: Coordinates
    ) -> Dict[Coordinates, str]:
        if (
            coordinate_dict[coordinates].isdigit()
            and (coordinates.x, coordinates.y + 1) in coordinate_dict.keys()
        ):
            acc_ = {
                **acc,
                **{coordinates: coordinate_dict[(coordinates.x, coordinates.y)]},
            }
            coordinates_ = Coordinates(coordinates.x, coordinates.y + 1)
            return get_full_number(acc_, coordinates_)
        elif coordinate_dict[coordinates].isdigit():
            return {**acc, **{coordinates: coordinate_dict[coordinates]}}
        else:
            return acc

    def adjacent_cells(coordinates: Coordinates) -> Dict[Coordinates, str]:
        x, y = coordinates
        adjacents_x = x - 1, x, x + 1
        adjacents_y = y - 1, y, y + 1
        adjacent_coordinates = [
            (i, j)
            for i in adjacents_x
            for j in adjacents_y
            if (i, j) in coordinate_dict.keys()
        ]
        return {
            coordinates: coordinate_dict[coordinates]
            for coordinates in adjacent_coordinates
        }

    def has_adjacent_symbols(number: Dict[Coordinates, str]):
        def coordinate_has_adjacent_symbols(coordinates: Coordinates):
            return any(
                adjacent_cell_coordinates in symbols.keys()
                for adjacent_cell_coordinates in adjacent_cells(coordinates).keys()
            )

        return any(
            coordinate_has_adjacent_symbols(coordinates)
            for coordinates in number.keys()
        )

    def value_to_left(coordinates: Coordinates) -> Optional[str]:
        return (
            coordinate_dict[(coordinates.x, coordinates.y - 1)]
            if (coordinates.x, coordinates.y - 1) in coordinate_dict.keys()
            else None
        )

    # find all numbers
    first_digits = {
        Coordinates(*k): v
        for k, v in coordinate_dict.items()
        if v.isdigit() and (value_to_left(k) is None or not value_to_left(k).isdigit())
    }
    numbers = [
        get_full_number({coordinates: value}, coordinates)
        for coordinates, value in first_digits.items()
    ]
    # find all symbols
    symbols = {
        Coordinates(*k): v
        for k, v in coordinate_dict.items()
        if v.isdigit() is False and v not in INVALID_CHARS
    }
    # filter numbers adjacent to symbols
    valid_numbers = [number for number in numbers if has_adjacent_symbols(number)]
    valid_numbers_int = [int("".join(n.values())) for n in valid_numbers]
    # get the sum
    return sum(int("".join(n.values())) for n in valid_numbers)


def part_two(input_):
    pass


if __name__ == "__main__":
    print(part_one(parsed_input()), part_two(parsed_input()))
    assert part_one(parsed_input()) == 535235
