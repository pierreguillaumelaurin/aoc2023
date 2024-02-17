from src.day08.day08 import part_one, part_two

EXAMPLE_PART_ONE = [
    "LLR",
    "",
    "AAA = (BBB, BBB)",
    "BBB = (AAA, ZZZ)",
    "ZZZ = (ZZZ, ZZZ)",
]

EXAMPLE_PART_TWO = [
    "LR",
    "",
    "11A = (11B, XXX)",
    "11B = (XXX, 11Z)",
    "11Z = (11B, XXX)",
    "22A = (22B, XXX)",
    "22B = (22C, 22C)",
    "22C = (22Z, 22Z)",
    "22Z = (22B, 22B)",
    "XXX = (XXX, XXX)",
]


def test_part_one():
    assert part_one(EXAMPLE_PART_ONE) == 6


def test_part_two():
    assert part_two(EXAMPLE_PART_TWO) == 6
