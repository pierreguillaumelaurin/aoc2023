from src.day09.day09 import part_one, part_two

EXAMPLE = ["0 3 6 9 12 15", "1 3 6 10 15 21", "10 13 16 21 30 45"]


def test_part_one():
    assert part_one(EXAMPLE) == 114


def test_part_two():
    assert part_two(EXAMPLE) == 2
