from collections import namedtuple
from typing import Dict, List

Coordinates = namedtuple("Coordinates", ["x", "y"])


def to_coordinates_dict(matrix: List[str]) -> Dict[Coordinates, str]:
    return {
        Coordinates(x, y): cell
        for x, line in enumerate(matrix)
        for y, cell in enumerate(line)
    }


def to_coordinates_dict(matrix: List[str]) -> Dict[Coordinates, str]:
    return {
        Coordinates(x, y): cell
        for x, line in enumerate(matrix)
        for y, cell in enumerate(line)
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
