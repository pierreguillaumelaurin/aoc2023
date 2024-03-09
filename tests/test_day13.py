from src.day13.day13 import (
    lines_above_horizontal_reflection_line,
    lines_above_vertical_reflection_line,
    parsed_input,
    part_one,
    part_two,
)

EXAMPLE = """
#.##..##.
..#.##.#.
##......#
##......#
..#.##.#.
..##..##.
#.#.##.#.

#...##..#
#....#..#
..##..###
#####.##.
#####.##.
..##..###
#....#..#
"""


def test_part_one():
    assert part_one(parsed_input(EXAMPLE)) == 405


def test_part_two():
    assert part_two(parsed_input(EXAMPLE)) == 400
