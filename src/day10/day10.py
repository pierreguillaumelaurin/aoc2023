from collections import defaultdict, deque
from typing import Dict, List, Tuple

from src.coordinates import Coordinates, to_coordinates_dict, translate
from src.utils import benchmark


def parsed_input():
    with open("./input.dat", "r") as data:
        return [line.strip() for line in data.readlines()]


# TODO combine first and last parameters to a tuple


class Maze:
    PIPE_VALUES = {"|", "-", "L", "J", "7", "F"}

    def __init__(self, coordinates: List[str]):
        self._map = to_coordinates_dict(coordinates)
        self.start = next((k, v) for k, v in self._map.items() if v == "S")
        self.start = self.start[0], self._get_start_pipe_kind(self.start[0])

    def _get_start_pipe_kind(self, start_coordinates: Coordinates):
        adjacent_pipe_coordinates = {
            coord
            for coord in self.get_adjacent_cells(start_coordinates)
            if self._map[coord] != "."
        }
        for hypothetical_value in self.PIPE_VALUES:
            hypothetical_entrances = self.get_entrances_coordinates(
                (start_coordinates, hypothetical_value)
            )
            if len(hypothetical_entrances.intersection(adjacent_pipe_coordinates)) == 2:
                return hypothetical_value
        else:
            raise Exception("Oupsi oupsa!")

    def get_adjacent_cells(self, coordinates: Coordinates) -> Dict[Coordinates, str]:
        x, y = coordinates
        adjacents_x = x - 1, x, x + 1
        adjacents_y = y - 1, y, y + 1
        adjacent_cells = {}
        for i in adjacents_x:
            if (i, y) in self._map.keys() and (i, y) != (x, y):
                adjacent_cells[(i, y)] = self._map[(i, y)]
        for j in adjacents_y:
            if (x, j) in self._map.keys() and (x, j) != (x, y):
                adjacent_cells[(x, j)] = self._map[(x, j)]
        return adjacent_cells

    def get_entrances_coordinates(self, pipe: Tuple[Coordinates, str]):
        _entrances = defaultdict(
            set,
            {
                "|": translate(pipe[0], {(-1, 0), (1, 0)}),
                "-": translate(pipe[0], {(0, -1), (0, 1)}),
                "L": translate(pipe[0], {(-1, 0), (0, 1)}),
                "J": translate(pipe[0], {(0, -1), (-1, 0)}),
                "7": translate(pipe[0], {(0, -1), (1, 0)}),
                "F": translate(pipe[0], {(1, 0), (0, 1)}),
            },
        )
        _entrances["S"] = _entrances[self.start[1]]

        return _entrances[pipe[1]]


@benchmark
def part_one(matrix: List[str]):
    maze = Maze(matrix)
    breadcrumb = set()
    current_key, current_value = maze.start
    while True:
        breadcrumb.add(current_key)
        adjacent_cells = maze.get_adjacent_cells(current_key)
        for k, v in adjacent_cells.items():
            if k not in breadcrumb and k in maze.get_entrances_coordinates(
                (current_key, current_value)
            ):
                current_key, current_value = (k, v)
                break
        else:
            break

    return int(len(breadcrumb) / 2)


def apply_shoelace_formula(coordinates: List[Coordinates]):
    def inner(i: int, coords: Coordinates):
        n = len(coordinates)
        _, y = coords
        return y * (coordinates[(i - 1) % n][0] - coordinates[(i + 1) % n][0])

    return abs(int(
        1 / 2 * sum(inner(i, coordinate) for i, coordinate in enumerate(coordinates))
    ))


def find_number_of_inner_points_with_pick_theorem(area: int, boundary_points: int):
    holes = 0
    return int(area - boundary_points / 2 - holes + 1)


@benchmark
def part_two(matrix: List[str]):
    maze = Maze(matrix)
    breadcrumb = []
    current_key, current_value = maze.start
    while True:
        breadcrumb.append(current_key)
        adjacent_cells = maze.get_adjacent_cells(current_key)
        for k, v in adjacent_cells.items():
            if k not in breadcrumb and k in maze.get_entrances_coordinates(
                (current_key, current_value)
            ):
                current_key, current_value = (k, v)
                break
        else:
            break

    area = int(apply_shoelace_formula(breadcrumb))

    return find_number_of_inner_points_with_pick_theorem(area, len(breadcrumb))


if __name__ == "__main__":
    assert part_one(parsed_input()) == 6903
    assert part_two(parsed_input()) == 265
    print(part_one(parsed_input()))
    print(part_two(parsed_input()))
