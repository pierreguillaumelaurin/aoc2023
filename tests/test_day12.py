from src.day12.day12 import (
    Converter,
    get_arrangements,
    get_number_of_valid_arrangements,
    part_one,
    satisfies,
)

EXAMPLE = [
    ("???.###", "1,1,3"),
    (".??..??...?##.", "1,1,3"),
    ("?#?#?#?#?#?#?#?", "1,3,1,6"),
    ("????.#...#...", "4,1,1"),
    ("????.######..#####.", "1,6,5"),
    ("?###????????", "3,2,1"),
]


class TestConverter:
    def test_to_state_symbol_when_starting_with_one(self):
        assert Converter.to_state_symbol("0b10") == "#."

    def test_to_state_symbol_when_starting_with_zero(self):
        assert Converter.to_state_symbol("0b00010") == "...#."

    def test_to_binary_when_starting_with_one(self):
        assert Converter.to_binary("#.") == "0b10"

    def test_to_binary_when_starting_with_zero(self):
        assert Converter.to_binary("...#.") == "0b00010"


def test_satisfies():
    assert satisfies([1, 2, 4], [4, 1, 2]) is True


def test_get_arrangements():
    assert sorted(get_arrangements("???.###")) == sorted(
        [
            "....###",
            "..#.###",
            ".#..###",
            ".##.###",
            "#...###",
            "#.#.###",
            "##..###",
            "###.###",
        ]
    )


def test_get_valid_arrangements():
    assert get_number_of_valid_arrangements("???.###", [1, 1, 3]) == 1
    assert get_number_of_valid_arrangements(".??..??...?##.", [1, 1, 3]) == 4
    assert get_number_of_valid_arrangements("?#?#?#?#?#?#?#?", [1, 3, 1, 6]) == 1


def test_part_one():
    assert part_one(EXAMPLE) == 21  # TODO fix
