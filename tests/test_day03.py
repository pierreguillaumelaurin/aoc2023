from src.day03.day03 import part_one, part_two

EXAMPLE = [
    "467..114..",
    "...*......",
    "..35..633.",
    "......#...",
    "617*......",
    ".....+.58.",
    "..592.....",
    "......755.",
    "...$.*....",
    ".664.598..",
]


def test_part_one():
    assert part_one(EXAMPLE) == 4361


def test_part_two():
    assert part_two(EXAMPLE) == 467835
