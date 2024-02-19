from collections import defaultdict, deque
from typing import Dict, List

from src.coordinates import Coordinates, to_coordinates_dict, translate
from src.utils import benchmark


def parsed_input():
    with open("./input.dat", "r") as data:
        return [line.strip() for line in data.readlines()]


# TODO isolate/rename, find better implementation
def get_adjacent_cells(
    coordinates_dict: Dict[Coordinates, str], coordinates: Coordinates
) -> Dict[Coordinates, str]:
    x, y = coordinates
    adjacents_x = x - 1, x, x + 1
    adjacents_y = y - 1, y, y + 1

    return {
        **{
            (i, y): coordinates_dict[(i, y)]
            for i in adjacents_x
            if (i, y) in coordinates_dict.keys() and (i, y) != (x, y)
        },
        **{
            (x, j): coordinates_dict[(x, j)]
            for j in adjacents_y
            if (x, j) in coordinates_dict.keys() and (x, j) != (x, y)
        },
    }


# TODO rename to differentiate better coords and value
def to_entrances_coordinates(coordinates: Coordinates, start_value: str, pipe: str):
    _entrances = defaultdict(
        set,
        {
            "|": {translate(coordinates, (-1, 0)), translate(coordinates, (1, 0))},
            "-": {translate(coordinates, (0, -1)), translate(coordinates, (0, 1))},
            "L": {translate(coordinates, (-1, 0)), translate(coordinates, (0, 1))},
            "J": {translate(coordinates, (0, -1)), translate(coordinates, (-1, 0))},
            "7": {translate(coordinates, (0, -1)), translate(coordinates, (1, 0))},
            "F": {translate(coordinates, (1, 0)), translate(coordinates, (0, 1))},
        },
    )
    _entrances["S"] = _entrances[start_value]

    return _entrances[pipe]


def start(maze: Dict[Coordinates, str]):
    return next((k, v) for k, v in maze.items() if v == "S")


# TODO remove do/while loop now that s is not in adjacent cells
@benchmark
def part_one(matrix: List[str]):
    coordinates_dict = to_coordinates_dict(matrix)
    breadcrumb = deque()
    current_key, current_value = start(coordinates_dict)
    while True:
        breadcrumb.append(current_key)
        adjacent_cells = get_adjacent_cells(coordinates_dict, current_key)
        for k, v in adjacent_cells.items():
            if k not in breadcrumb and current_key in to_entrances_coordinates(coordinates=k, start_value=v, pipe=v):
                current_key, current_value = (k, v)
                print("worked")
                break
        else:
            break
        if current_value == "S":
            break

    print(breadcrumb)
    return len(breadcrumb) / 2


if __name__ == "__main__":
    print(part_one(parsed_input()))
