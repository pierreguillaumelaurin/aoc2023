from src.day06.day06 import part_one

EXAMPLE = ["Time:      7  15   30", "Distance:  9  40  200"]


def test_part_one():
    assert part_one(EXAMPLE) == 288
