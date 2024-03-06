from collections import defaultdict
from copy import deepcopy
from typing import List

from src.utils import benchmark


def parsed_input():
    with open("./input.dat", "r") as data:
        return [[cell for cell in line.strip()] for line in data.readlines()]


def with_rocks_moved_north(lines: List[List[str]]):
    _matrix = deepcopy(lines)
    latest_obstacle_row_by_column = defaultdict(lambda: -1)

    for i, row in enumerate(_matrix):
        for j, cell in enumerate(row):
            match cell:
                case "#":
                    latest_obstacle_row_by_column[j] = i
                case "O" if latest_obstacle_row_by_column[j] == i - 1:
                    latest_obstacle_row_by_column[j] += 1
                case "O":
                    _matrix[latest_obstacle_row_by_column[j] + 1][j] = "O"
                    _matrix[i][j] = "."
                    latest_obstacle_row_by_column[j] += 1
                case ".":
                    pass
                case _:
                    raise ValueError(f"invalid value {cell} at row {i} on column {j}.")
    return _matrix


def total_load(matrix: List[List[str]]):
    def single_rock_load(rock_index: int):
        return len(matrix) - rock_index

    return sum(
        single_rock_load(i)
        for i, row in enumerate(matrix)
        for cell in row
        if cell == "O"
    )


@benchmark
def part_one(lines: List[List[str]]):
    return total_load(with_rocks_moved_north(lines))


@benchmark
def part_two(lines: List[str]):
    pass


if __name__ == "__main__":
    print(part_one(parsed_input()))
