import sys
from collections import deque
from typing import List, Set, Tuple

from src.coordinates import Coordinates, add_coordinates, to_coordinates_dict
from src.utils import benchmark


def parsed_input():
    with open("./input.dat", "r") as data:
        return [line.strip() for line in data.readlines()]


class Matrix:
    def __init__(self, matrix: List[str]):
        self._map = to_coordinates_dict(matrix)

    def get_energized_tile_count(
        self, start: Coordinates, starting_direction: Coordinates
    ):
        def is_in_loop(
            move: Coordinates,
            direction: Coordinates,
            moves_already_made: Set[Coordinates],
        ):
            print(moves_already_made)
            return (move, direction) in moves_already_made

        moves_already_made = set()
        first_move = (start, starting_direction)
        moves_to_make = deque()
        moves_to_make.append(first_move)
        while moves_to_make:
            move, direction = moves_to_make.popleft()
            if move not in self._map.keys() or (move, direction) in moves_already_made:
                continue
            moves_already_made.add((move, direction))
            match self._map[move]:
                case ".":
                    next_move = add_coordinates(move, direction)
                    moves_to_make.append((next_move, direction))
                case "|" if abs(direction[0]) == 1 and direction[1] == 0:
                    next_move = add_coordinates(move, direction)
                    moves_to_make.append((next_move, direction))
                case "-" if direction[0] == 0 and abs(direction[1]) == 1:
                    next_move = add_coordinates(move, direction)
                    moves_to_make.append((next_move, direction))
                case "/":
                    next_direction = (-1 * direction[1], -1 * direction[0])
                    next_move = add_coordinates(move, next_direction)
                    moves_to_make.append((next_move, next_direction))
                case "\\":
                    next_direction = (direction[1], direction[0])
                    next_move = add_coordinates(move, next_direction)
                    moves_to_make.append((next_move, next_direction))
                case "|":
                    next_first_direction = (
                        direction[1],
                        direction[0],
                    )  # TODO use function composability instead
                    next_first_move = add_coordinates(move, next_first_direction)
                    next_second_direction = (-1 * direction[1], -1 * direction[0])
                    next_second_move = add_coordinates(move, next_second_direction)
                    moves_to_make.append((next_first_move, next_first_direction))
                    moves_to_make.append((next_second_move, next_second_direction))
                case "-":
                    next_first_direction = (
                        direction[1],
                        direction[0],
                    )  # TODO use function composability instead
                    next_first_move = add_coordinates(move, next_first_direction)
                    next_second_direction = (-1 * direction[1], -1 * direction[0])
                    next_second_move = add_coordinates(move, next_second_direction)
                    moves_to_make.append((next_first_move, next_first_direction))
                    moves_to_make.append((next_second_move, next_second_direction))
                case _:
                    raise ValueError(
                        f"Oops! Here is the context: next move={move}, direction={direction}"
                    )

        return len({coordinate for coordinate, _ in moves_already_made})


@benchmark
def part_one(raw_matrix: List[str]):
    matrix = Matrix(raw_matrix)
    return matrix.get_energized_tile_count((0, 0), (0, 1))


@benchmark
def part_two(raw_matrix: List[str]):
    matrix = Matrix(raw_matrix)
    max_left_side = max(
        matrix.get_energized_tile_count((i, 0), (0, 1)) for i in range(len(raw_matrix))
    )
    max_right_side = max(
        matrix.get_energized_tile_count((i, len(raw_matrix[0]) - 1), (0, -1))
        for i in range(len(raw_matrix))
    )
    max_top_side = max(
        matrix.get_energized_tile_count((0, i), (1, 0)) for i in range(len(raw_matrix))
    )
    max_bottom_side = max(
        matrix.get_energized_tile_count((len(raw_matrix) - 1, i), (-1, 0))
        for i in range(len(raw_matrix))
    )
    print(max_left_side, max_right_side, max_top_side, max_bottom_side)
    return max(max_left_side, max_right_side, max_top_side, max_bottom_side)


if __name__ == "__main__":
    print(part_one(parsed_input()))
    print(part_two(parsed_input()))
