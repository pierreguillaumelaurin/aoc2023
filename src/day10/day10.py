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
    adjacent_cells = {}
    for i in adjacents_x:
        if (i, y) in coordinates_dict.keys() and (i, y) != (x, y):
            adjacent_cells[(i, y)] = coordinates_dict[(i, y)]
    for j in adjacents_y:
        if (x, j) in coordinates_dict.keys() and (x, j) != (x, y):
            adjacent_cells[(x, j)] = coordinates_dict[(x, j)]
    return adjacent_cells


pipe_values = {"|", "-", "L", "J", "7", "F"}


def get_start_pipe_kind(
        coordinates_dict: Dict[Coordinates, str], start_coordinates: Coordinates
):
    adjacent_pipe_coordinates = {
        coord
        for coord in get_adjacent_cells(coordinates_dict, start_coordinates)
        if coordinates_dict[coord] != "."
    }
    for hypothetical_value in pipe_values:
        hypothetical_entrances = to_entrances_coordinates(
            start_coordinates, ".", hypothetical_value
        )
        if len(hypothetical_entrances.intersection(adjacent_pipe_coordinates)) == 2:
            return hypothetical_value
    else:
        raise Exception("Oupsi oupsa!")


# TODO combine first and last parameters to a tuple
def to_entrances_coordinates(coordinates: Coordinates, start_value: str, pipe: str):
    _entrances = defaultdict(
        set,
        {
            "|": translate(coordinates, {(-1, 0), (1, 0)}),
            "-": translate(coordinates, {(0, -1), (0, 1)}),
            "L": translate(coordinates, {(-1, 0), (0, 1)}),
            "J": translate(coordinates, {(0, -1), (-1, 0)}),
            "7": translate(coordinates, {(0, -1), (1, 0)}),
            "F": translate(coordinates, {(1, 0), (0, 1)}),
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
    breadcrumb = set()
    starting_value = start(coordinates_dict)
    start_pipe_kind = get_start_pipe_kind(coordinates_dict, starting_value[0])
    current_key, current_value = starting_value
    while True:
        breadcrumb.add(current_key)
        adjacent_cells = get_adjacent_cells(coordinates_dict, current_key)
        for k, v in adjacent_cells.items():
            if k not in breadcrumb and k in to_entrances_coordinates(
                    coordinates=current_key, start_value=start_pipe_kind, pipe=current_value
            ):
                current_key, current_value = (k, v)
                break
        else:
            break

    assert len(breadcrumb) % 2 == 0
    return int(len(breadcrumb) / 2)


# TODO remove?
def connects(current_key, current_value, k, start_pipe_kind, v):
    return current_key in to_entrances_coordinates(
        coordinates=k, start_value=start_pipe_kind, pipe=v
    ) and k in to_entrances_coordinates(current_key, start_pipe_kind, current_value)


if __name__ == "__main__":
    assert part_one(parsed_input()) == 6903
    print(part_one(parsed_input()))
