from copy import deepcopy
from typing import List

from src.utils import benchmark


def parsed_input(data: str):
    return [raw_matrix.strip().split("\n") for raw_matrix in data.split("\n\n")]


def rotate_left(matrix: List[str]):
    return [list(t) for t in zip(*matrix)]


def lines_above_horizontal_reflection_line(matrix: List[list | str]):
    for i in range(1, len(matrix)):
        above = matrix[:i][::-1]
        below = matrix[i:]

        symmetrical_part_above = above[: len(below)]
        symmetrical_part_below = below[: len(above)]
        if symmetrical_part_above == symmetrical_part_below:
            return i
    return 0


def lines_above_horizontal_reflection_line_when_removing_smudge(
    matrix: List[list | str],
):
    def cell_mismatches_count(row_above: List[str], row_below: List[str]):
        return sum(
            0 if cell_above == cell_below else 1
            for cell_above, cell_below in zip(row_above, row_below)
        )

    for i in range(1, len(matrix)):
        above = matrix[:i][::-1]
        below = matrix[i:]

        if (
            sum(
                cell_mismatches_count(row_above, row_below)
                for row_above, row_below in zip(above, below)
            )
            == 1
        ):
            return i
    return 0


def lines_above_vertical_reflection_line_when_removing_smudge(matrix: List[list | str]):
    return lines_above_horizontal_reflection_line_when_removing_smudge(
        rotate_left(matrix)
    )


def lines_above_vertical_reflection_line(matrix: List[str]):
    return lines_above_horizontal_reflection_line(rotate_left(matrix))


@benchmark
def part_one(matrixes: List[List[str]]):
    return sum(
        lines_above_vertical_reflection_line(matrix)
        or (100 * lines_above_horizontal_reflection_line(matrix))
        for matrix in matrixes
    )


@benchmark
def part_two(matrixes: List[List[str]]):
    return sum(
        lines_above_vertical_reflection_line_when_removing_smudge(matrix)
        or (100 * lines_above_horizontal_reflection_line_when_removing_smudge(matrix))
        for matrix in matrixes
    )


if __name__ == "__main__":
    with open("./input.dat", "r") as file:
        raw_input = file.read()
        print(part_one(parsed_input(raw_input)))
        assert part_one(parsed_input(raw_input)) == 34821
        print(part_two(parsed_input(raw_input)))
        assert part_two(parsed_input(raw_input)) == 36919
