from itertools import combinations
from typing import List, Set

from src.coordinates import Coordinates, to_coordinates_dict
from src.utils import benchmark


def parsed_input():
    with open("./input.dat", "r") as data:
        return [line.strip() for line in data.readlines()]


class Matrix:
    def __doc__(self):
        """
        «L’entièreté de l’univers nous est donnée par milliards de fragments s’ouvrant chacun sur d’autres univers.»

        — Michel X Côté, Un poète chez les éleveurs de pickups
        """

    def __init__(self, matrix: List[str]):
        self._map = to_coordinates_dict(matrix)
        self._empty_columns = self._get_empty_columns()
        self._empty_rows = self._get_empty_rows()

    def _get_column_values(self, i: int) -> List[str]:
        max_column_index = max(coord[0] for coord in self._map.keys())
        return [self._map[(c, i)] for c in range(max_column_index + 1)]

    def _get_empty_columns(self) -> Set[int]:
        def is_empty_column(i: int):
            return all(v != "#" for v in self._get_column_values(i))

        return {
            i
            for i in range(max(coord[0] for coord in self._map.keys()))
            if is_empty_column(i)
        }

    def _get_row_values(self, i: int) -> List[str]:
        max_row_index = max(coord[1] for coord in self._map.keys())
        return [self._map[(i, c)] for c in range(max_row_index + 1)]

    def _get_empty_rows(self) -> Set[int]:
        def is_empty_row(i: int):
            return all(v != "#" for v in self._get_row_values(i))

        return {
            i
            for i in range(max(coord[1] for coord in self._map.keys()))
            if is_empty_row(i)
        }

    def get_galaxy_pairs(self):
        galaxies_coordinates = {k for k, v in self._map.items() if v == "#"}

        return combinations(galaxies_coordinates, 2)

    def find_shortest_path_length(
        self, source: Coordinates, destination: Coordinates, galaxies_weight=1
    ):
        path_length = abs(destination[0] - source[0]) + abs(destination[1] - source[1])

        columns_needing_ajustments_crossed = len(
            {
                c
                for c in self._empty_columns
                if destination[1] < c < source[1] or source[1] < c < destination[1]
            }
        )
        rows_needing_ajustments_crossed = len(
            {
                r
                for r in self._empty_rows
                if destination[0] < r < source[0] or source[0] < r < destination[0]
            }
        )

        return (
            path_length
            + columns_needing_ajustments_crossed * galaxies_weight
            + rows_needing_ajustments_crossed * galaxies_weight
        )


@benchmark
def part_one(raw_matrix: List[str]):
    matrix = Matrix(raw_matrix)
    return sum(
        matrix.find_shortest_path_length(source, destination)
        for source, destination in matrix.get_galaxy_pairs()
    )


@benchmark
def part_two(raw_matrix: List[str]):
    matrix = Matrix(raw_matrix)
    return sum(
        matrix.find_shortest_path_length(source, destination, galaxies_weight=999_999)
        for source, destination in matrix.get_galaxy_pairs()
    )


if __name__ == "__main__":
    assert part_one(parsed_input()) == 9686930
    print(part_one(parsed_input()))
    assert part_two(parsed_input()) == 630728425490
    print(part_two(parsed_input()))
