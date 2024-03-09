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


def rotate_right(matrix: List[List[str]]):
    return [list(t) for t in zip(*reversed(matrix))]


def with_rocks_moved_west(matrix: List[List[str]]):
    return rotate_right(
        rotate_right(rotate_right(with_rocks_moved_north(rotate_right(matrix))))
    )


def with_rocks_moved_south(matrix: List[List[str]]):
    return rotate_right(
        rotate_right(with_rocks_moved_north(rotate_right(rotate_right(matrix))))
    )


def with_rocks_moved_east(matrix: List[List[str]]):
    return rotate_right(
        with_rocks_moved_north(rotate_right(rotate_right(rotate_right(matrix))))
    )


def do_cycle(matrix: List[List[str]]):
    return with_rocks_moved_east(
        with_rocks_moved_south(with_rocks_moved_west(with_rocks_moved_north(matrix)))
    )


def get_count_before_loop_starts(matrix: List[List[str]]):
    pass_cycle_results = []
    count = 0
    result = do_cycle(matrix)
    while True:
        result = do_cycle(result)
        count += 1
        if result in pass_cycle_results:
            break
        pass_cycle_results.append(result)
    return count


def to_state_at_loop_beginning(matrix: List[List[str]], count_before_loop_starts: int):
    result = matrix
    for _ in range(count_before_loop_starts - 1):
        result = do_cycle(result)
    return result


def get_count_for_loop_to_reset(matrix: List[List[str]], count_before_loop_starts: int):
    count = 0

    result = to_state_at_loop_beginning(matrix, count_before_loop_starts)
    loop_beginning = result
    while True:
        result = do_cycle(result)
        count += 1
        if loop_beginning == result:
            break
    return count


@benchmark
def part_one(lines: List[List[str]]):
    return total_load(with_rocks_moved_north(lines))


@benchmark
def part_two(lines: List[List[str]]):
    count_before_loop_starts = get_count_before_loop_starts(lines)
    count = get_count_for_loop_to_reset(lines, count_before_loop_starts)
    number_of_cycle_equivalent_to_a_billion = (
            (1_000_000_000 - count_before_loop_starts) % count
    )
    matrix = lines
    for _ in range(count_before_loop_starts + number_of_cycle_equivalent_to_a_billion):
        matrix = do_cycle(matrix)
    return total_load(matrix)


if __name__ == "__main__":
    print(part_one(parsed_input()))
    assert part_two(parsed_input()) == 108404
    print(part_two(parsed_input()))
