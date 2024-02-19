from src.day10.day10 import part_one

# fmt: off
FIRST_EXAMPLE = [
     ".....",
     ".S-7.",
     ".|.|.",
     ".L-J.",
     "....."
]

SECOND_EXAMPLE = [
    "..F7.",
    ".FJ|.",
    "SJ.L7",
    "|F--J",
    "LJ..."
]
# fmt: on


def test_part_one_first_example():
    assert part_one(FIRST_EXAMPLE) == 4


def test_part_one_second_example():
    assert part_one(SECOND_EXAMPLE) == 8
