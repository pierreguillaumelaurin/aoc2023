from typing import List

from src.coordinates import Coordinates
from src.utils import benchmark


def parsed_input():
    with open("./input.dat", "r") as data:
        return [line.strip() for line in data.readlines()]


def get_adjacent_cells(coordinates: Coordinates, matrix: List[List[str]]):
    x, y = coordinates
    adjacent_cells = ((x, y - 1), (x, y + 1), (x - 1, y), (x + 1, y))
    return [
        (r, c)
        for (r, c) in adjacent_cells
        if 0 < r < len(matrix) and 0 < c < len(matrix[0])
    ]


def get_reachable_garden_plots(matrix: List[List[str]], starting_position: Coordinates, required_steps: int):
    reachable_garden_plots = {starting_position}

    for _ in range(required_steps):
        reachable_garden_plots = {
            (x, y)
            for plot in reachable_garden_plots
            for (x, y) in get_adjacent_cells(plot, matrix)
            if matrix[x][y] != "#"
        }
    return len(reachable_garden_plots)

@benchmark
def part_one(matrix: List[List[str]], required_steps=64):
    starting_position = next(
        (i, j)
        for i, row in enumerate(matrix)
        for j, cell in enumerate(row)
        if cell == "S"
    )

    return get_reachable_garden_plots(matrix, starting_position=starting_position, required_steps=required_steps)


@benchmark
def part_two(matrix: List[List[str]], required_steps=64):
    pass


if __name__ == "__main__":
    assert part_one(parsed_input()) == 3737
    print(part_one(parsed_input(), 26501365))
    assert part_two(parsed_input()) == 26501365
