from src.day08.day08 import part_one

EXAMPLE = [
    "LLR",
    "",
    "AAA = (BBB, BBB)",
    "BBB = (AAA, ZZZ)",
    "ZZZ = (ZZZ, ZZZ)"
]


def test_part_one():
    assert part_one(EXAMPLE) == 6
