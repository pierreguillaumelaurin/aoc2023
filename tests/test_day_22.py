from src.day22.day22 import get_overlap, has_overlap_above, part_one, part_two

RAW_EXAMPLE = [
    (1, 0, 1, 1, 2, 1),
    (0, 0, 2, 2, 0, 2),
    (0, 2, 3, 2, 2, 3),
    (0, 0, 4, 0, 2, 4),
    (2, 0, 5, 2, 2, 5),
    (0, 1, 6, 2, 1, 6),
    (1, 1, 8, 1, 1, 9),
]

PARSED_EXAMPLE = [
    ((1, 0, 1), (1, 2, 1)),
    ((0, 0, 2), (2, 0, 2)),
    ((0, 2, 3), (2, 2, 3)),
    ((0, 0, 4), (0, 2, 4)),
    ((2, 0, 5), (2, 2, 5)),
    ((0, 1, 6), (2, 1, 6)),
    ((1, 1, 8), (1, 1, 9)),
]


def test_has_overlap_when_overlap_exists():
    assert get_overlap(PARSED_EXAMPLE[0], PARSED_EXAMPLE) == [
        ((1, 0, 1), (1, 2, 1)),
        ((0, 0, 2), (2, 0, 2)),
        ((0, 2, 3), (2, 2, 3)),
        ((0, 1, 6), (2, 1, 6)),
        ((1, 1, 8), (1, 1, 9)),
    ]


def test_has_overlap_when_overlap_does_not_exist():
    a_non_overlaping_block = ((2, 0, 5), (2, 2, 5))
    assert get_overlap(PARSED_EXAMPLE[-1], [a_non_overlaping_block]) == []


def test_has_overlap_above_when_overlap_exists():
    assert has_overlap_above(PARSED_EXAMPLE[1], PARSED_EXAMPLE) is True


def test_has_overlap_above_when_overlap_does_not_exist():
    assert has_overlap_above(PARSED_EXAMPLE[-1], PARSED_EXAMPLE) is False


def test_part_one():
    assert part_one(RAW_EXAMPLE) == 5

def test_part_two():
    assert part_two(RAW_EXAMPLE) == 7
