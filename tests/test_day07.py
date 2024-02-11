from src.day07.day07 import part_one, part_two

EXAMPLE = [
    "32T3K 765",
    "T55J5 684",
    "KK677 28",
    "KTJJT 220",
    "QQQJA 483",
]


def test_part_one():
    assert part_one(EXAMPLE) == 6440


def test_part_two():
    assert part_two(EXAMPLE) == 5905
