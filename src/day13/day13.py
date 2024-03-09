from typing import List

from src.utils import benchmark


def parsed_input(data: str):
    return [raw_matrix.strip().split("\n") for raw_matrix in data.split("\n\n")]


def rotate_left(matrix: List[str]):
    return [list(t) for t in zip(*matrix)]


def lines_above_horizontal_reflection_line(matrix: List[list | str]):
    def is_horizontal_index(one_based_index: int):
        if len(matrix[:one_based_index]) < len(matrix[one_based_index:]):
            return matrix[:one_based_index] == list(
                reversed(matrix[one_based_index : one_based_index * 2])
            )
        symmetry_beginning_index = one_based_index - len(matrix[one_based_index:])
        return matrix[symmetry_beginning_index:one_based_index] == list(
            reversed(matrix[one_based_index:])
        )

    horizontal_line_indexes_candidates = [
        i for i in range(len(matrix[:-1])) if matrix[i] == matrix[i + 1]
    ]
    return (
        next(
            (
                i
                for i in horizontal_line_indexes_candidates
                if is_horizontal_index(one_based_index := i + 1)
            ),
            -1,
        )
        + 1
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
def part_two(matrixes: List[List[List[str]]]):
    pass


if __name__ == "__main__":
    with open("./input.dat", "r") as file:
        raw_input = file.read()
        print(part_one(parsed_input(raw_input)))
        assert part_one(parsed_input(raw_input)) == 34821
