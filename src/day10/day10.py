from src.utils import benchmark


def parsed_input():
    with open("./input.dat", "r") as data:
        return [line.strip() for line in data.readlines()]


destinations_with_left_hand_on_wall = {
    "|": ("|"),
    "-": ("-"),
    "L": (),
    "J": (),
    "7": (),
    "F": (),
    "S": ()
}


@benchmark
def part_one():
    pass
