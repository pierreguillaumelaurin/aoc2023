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

        symmetrical_part_above = above[:len(below)]
        symmetrical_part_below = below[:len(above)]
        if symmetrical_part_above == symmetrical_part_below:
            return i
    return 0


def lines_above_vertical_reflection_line(matrix: List[str]):
    return lines_above_horizontal_reflection_line(rotate_left(matrix))


@benchmark
def part_one(matrixes: List[List[str]]):
    return sum(
        lines_above_vertical_reflection_line(matrix)
        or (100 * lines_above_horizontal_reflection_line(matrix))
        for matrix in matrixes
    )


def switched(character: str):
    match character:
        case ".":
            return "#"
        case "#":
            return "."
        case _:
            raise ValueError("Invalid character!", character)


def lines_above_vertical_reflection_line_when_controlling_for_smudge(matrix: List[str]):
    original_result = lines_above_vertical_reflection_line(matrix)
    for i in range(len(rotate_left(matrix))):
        for j in range(len(rotate_left(matrix)[i])):
            modified_matrix = [[cell for cell in line] for line in rotate_left(matrix)]
            modified_matrix[i][j] = switched(modified_matrix[i][j])
            if (
                    lines_above_vertical_reflection_line(modified_matrix)
                    != 0 and lines_above_vertical_reflection_line(modified_matrix) != original_result
            ):
                return lines_above_vertical_reflection_line(modified_matrix)
            if (
                lines_above_horizontal_reflection_line(modified_matrix)
                != 0
            ):
                return lines_above_horizontal_reflection_line(modified_matrix)
    return 0


def lines_above_horizontal_reflection_line_when_controlling_for_smudge(
    matrix: List[str],
):
    original_result = lines_above_horizontal_reflection_line(matrix)
    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            modified_matrix = [[cell for cell in line] for line in matrix]
            modified_matrix[i][j] = switched(modified_matrix[i][j])
            if (
                lines_above_horizontal_reflection_line(modified_matrix)
                != 0 and lines_above_horizontal_reflection_line(modified_matrix) != original_result
            ):
                return lines_above_horizontal_reflection_line(modified_matrix)
            if (
                    lines_above_vertical_reflection_line(modified_matrix)
                    != 0
            ):
                return lines_above_vertical_reflection_line(modified_matrix)
    return 0


@benchmark
def part_two(matrixes: List[List[str]]):
    print('errors',  len(list(test for matrix in matrixes if (test :=  (
            100
            * lines_above_horizontal_reflection_line_when_controlling_for_smudge(matrix)
        ) or lines_above_vertical_reflection_line_when_controlling_for_smudge(matrix)) == 0)))


    return sum(
        (
            100
            * lines_above_horizontal_reflection_line_when_controlling_for_smudge(matrix)
        ) or lines_above_vertical_reflection_line_when_controlling_for_smudge(matrix)
        for matrix in matrixes
    )


if __name__ == "__main__":
    with open("./input.dat", "r") as file:
        raw_input = file.read()
        print(part_one(parsed_input(raw_input)))
        assert part_one(parsed_input(raw_input)) == 34821
        print(part_two(parsed_input(raw_input)))
