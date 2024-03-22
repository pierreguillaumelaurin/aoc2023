from typing import List, Literal

from src.coordinates import Coordinates, add_coordinates, multiply_coordinates
from src.utils import benchmark


def parsed_input():
    with open("./input.dat", "r") as data:
        return [line.strip() for line in data.readlines()]


def to_direction(acronym: Literal["U", "R", "D", "L"]):
    match acronym:
        case "0":
            return (0, 1)
        case "1":
            return (1, 0)
        case "2":
            return (0, -1)
        case "3":
            return (-1, 0)
        case "L":
            return (0, -1)
        case "U":
            return (-1, 0)
        case "R":
            return (0, 1)
        case "D":
            return (1, 0)
        case "L":
            return (0, -1)
        case _:
            raise Exception("Oops, an invalid acronym appeared:", acronym)


def apply_shoelace_formula(coordinates: List[Coordinates]):
    def inner(i: int, coords: Coordinates):
        n = len(coordinates)
        _, y = coords
        return y * (coordinates[(i - 1) % n][0] - coordinates[(i + 1) % n][0])

    return abs(
        int(
            1
            / 2
            * sum(inner(i, coordinate) for i, coordinate in enumerate(coordinates))
        )
    )


def find_number_of_inner_points_with_pick_theorem(area: int, boundary_points: int):
    holes = 0
    return int(area - boundary_points / 2 - holes + 1)


@benchmark
def part_one(matrix: List[str]):
    # get perimeter positions and value
    corner_positions = [(0, 0)]
    perimeter_length = 0
    for line in matrix:
        acronym, meters, _ = line.split()
        next_corner_position = add_coordinates(
            corner_positions[-1],
            multiply_coordinates(to_direction(acronym), (int(meters), int(meters))),
        )
        corner_positions.append(next_corner_position)
        perimeter_length += int(meters)
    # total value
    area = apply_shoelace_formula(corner_positions)
    inner_area = find_number_of_inner_points_with_pick_theorem(area, perimeter_length)

    return perimeter_length + inner_area


def hexa_list_to_int(meters: str):
    return int("".join(meters), 16)


@benchmark
def part_two(matrix: List[str]):
    # get perimeter positions and value
    corner_positions = [(0, 0)]
    perimeter_length = 0
    for line in matrix:
        *meters, acronym = line[line.index("#") + 1 : -1]
        next_corner_position = add_coordinates(
            corner_positions[-1],
            multiply_coordinates(
                to_direction(acronym),
                (hexa_list_to_int(meters), hexa_list_to_int(meters)),
            ),
        )
        corner_positions.append(next_corner_position)
        perimeter_length += hexa_list_to_int(meters)
    # total value
    area = apply_shoelace_formula(corner_positions)
    inner_area = find_number_of_inner_points_with_pick_theorem(area, perimeter_length)

    return perimeter_length + inner_area


if __name__ == "__main__":
    assert part_one(parsed_input()) == 50746
    print(part_one(parsed_input()))
    assert part_two(parsed_input()) == 70086216556038
    print(part_two(parsed_input()))
