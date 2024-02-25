from src.day10.day10 import part_one, part_two

# fmt: off
PART_ONE_FIRST_EXAMPLE = [
     ".....",
     ".S-7.",
     ".|.|.",
     ".L-J.",
     "....."
]

PART_ONE_SECOND_EXAMPLE = [
    "..F7.",
    ".FJ|.",
    "SJ.L7",
    "|F--J",
    "LJ..."
]


# fmt: on
PART_TWO_FIRST_EXAMPLE = [
    "...........",
    ".S-------7.",
    ".|F-----7|.",
    ".||.....||.",
    ".||.....||.",
    ".|L-7.F-J|.",
    ".|..|.|..|.",
    ".L--J.L--J.",
    "...........",
]


def test_part_one_first_example():
    assert part_one(PART_ONE_FIRST_EXAMPLE) == 4


def test_part_one_second_example():
    assert part_one(PART_ONE_SECOND_EXAMPLE) == 8


def test_part_two_first_example():
    assert part_two(PART_TWO_FIRST_EXAMPLE) == 4
