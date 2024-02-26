from itertools import combinations
from typing import List

import pytest

from src.day11.day11 import Matrix, part_one, part_two

EXAMPLE = [
    "...#......",
    ".......#..",
    "#.........",
    "..........",
    "......#...",
    ".#........",
    ".........#",
    "..........",
    ".......#..",
    "#...#.....",
]


class TestMatrix:
    @pytest.fixture
    def matrix_from_example(self):
        return Matrix(EXAMPLE)

    def test_empty_columns(self, matrix_from_example):
        assert matrix_from_example.get_empty_columns() == {2, 5, 8}

    def test_empty_rows(self, matrix_from_example):
        assert matrix_from_example.get_empty_rows() == {3, 7}

    def test_find_shortest_path_length(self, matrix_from_example):
        assert matrix_from_example.find_shortest_path_length((0, 3), (1, 7)) == 6

def test_part_one():
    assert part_one(EXAMPLE) == 374
