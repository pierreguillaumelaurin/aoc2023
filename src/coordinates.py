from collections import namedtuple
from typing import Dict, List

Coordinates = namedtuple("Coordinates", ["x", "y"])


def to_coordinates_dict(matrix: List[str]) -> Dict[Coordinates, str]:
    return {
        Coordinates(x, y): cell
        for x, line in enumerate(matrix)
        for y, cell in enumerate(line)
    }


def add_coordinates(first: Coordinates, second: Coordinates):
    return Coordinates(first[0] + second[0], first[1] + second[1])

def substract_coordinates(first: Coordinates, second: Coordinates):
    return Coordinates(first[0] - second[0], first[1] - second[1])

def translate(base: Coordinates, coordinates: set[Coordinates]):
    def _translate(left_coord: Coordinates, right_coord: Coordinates):
        return Coordinates(
            left_coord[0] + right_coord[0], left_coord[1] + right_coord[1]
        )

    return {_translate(base, coordinate) for coordinate in coordinates}


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
