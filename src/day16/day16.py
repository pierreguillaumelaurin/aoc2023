import sys
from typing import List, Set

from src.coordinates import Coordinates, add_coordinates, to_coordinates_dict
from src.utils import benchmark

sys.setrecursionlimit(20000)


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
            move: Coordinates, direction: Coordinates, energized_tiles: Set[Coordinates]
        ):
            previous_move = add_coordinates(
                move, (-1 * direction[0], -1 * direction[0])
            )

            return (
                move in self._map.keys()
                and previous_move in self._map.keys()
                and (
                    (self._map[previous_move] == "|" and abs(direction[0]) == 1)
                    or (self._map[previous_move] == "-" and abs(direction[1]) == 1)
                )
                and previous_move in energized_tiles
                and move in energized_tiles
            )

        def next_moves(
            move: Coordinates, direction: Coordinates, energized_tiles: Set[Coordinates]
        ):
            if move not in self._map.keys() or is_in_loop(
                move, direction, energized_tiles
            ):
                return energized_tiles
            print(is_in_loop(move, direction, energized_tiles))
            match self._map[move]:
                case ".":
                    next_move = add_coordinates(move, direction)
                    return next_moves(next_move, direction, energized_tiles | {move})
                case "|" if abs(direction[0]) == 1 and direction[1] == 0:
                    next_move = add_coordinates(move, direction)
                    return next_moves(next_move, direction, energized_tiles | {move})
                case "-" if direction[0] == 0 and abs(direction[1]) == 1:
                    next_move = add_coordinates(move, direction)
                    return next_moves(next_move, direction, energized_tiles | {move})
                case "/":
                    next_direction = (-1 * direction[1], -1 * direction[0])
                    next_move = add_coordinates(move, next_direction)
                    return next_moves(
                        next_move, next_direction, energized_tiles | {move}
                    )
                case "\\":
                    next_direction = (direction[1], direction[0])
                    next_move = add_coordinates(move, next_direction)
                    return next_moves(
                        next_move, next_direction, energized_tiles | {move}
                    )
                case "|":
                    next_first_direction = (
                        direction[1],
                        direction[0],
                    )  # TODO use function composability instead
                    next_first_move = add_coordinates(move, next_first_direction)
                    next_second_direction = (-1 * direction[1], -1 * direction[0])
                    next_second_move = add_coordinates(move, next_second_direction)
                    return next_moves(
                        next_first_move, next_first_direction, energized_tiles | {move}
                    ) | next_moves(
                        next_second_move,
                        next_second_direction,
                        energized_tiles | {move},
                    )
                case "-":
                    next_first_direction = (
                        direction[1],
                        direction[0],
                    )  # TODO use function composability instead
                    next_first_move = add_coordinates(move, next_first_direction)
                    next_second_direction = (-1 * direction[1], -1 * direction[0])
                    next_second_move = add_coordinates(move, next_second_direction)
                    return next_moves(
                        next_first_move, next_first_direction, energized_tiles | {move}
                    ) | next_moves(
                        next_second_move,
                        next_second_direction,
                        energized_tiles | {move},
                    )
                case _:
                    raise ValueError(
                        f"Oops! Here is the context: next move={move}, direction={direction}"
                    )

        return len(next_moves(start, starting_direction, set()))


@benchmark
def part_one(raw_matrix: List[str]):
    matrix = Matrix(raw_matrix)
    return matrix.get_energized_tile_count((0, 0), (0, 1))


if __name__ == "__main__":
    print(part_one(parsed_input()))
