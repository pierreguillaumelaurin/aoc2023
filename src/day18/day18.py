from typing import List, Literal

from src.coordinates import Coordinates, add_coordinates
from src.utils import benchmark


def parsed_input():
    with open("./input.dat", "r") as data:
        return [line.strip() for line in data.readlines()]


def to_direction(acronym: Literal['U', 'R', 'D', 'L']):
    match acronym:
        case 'U':
            return (-1, 0)
        case 'R':
            return (0, 1)
        case 'D':
            return (1, 0)
        case 'L':
            return (0, -1)
        case _:
            raise ('Oops, an invalid acronym appeared:', acronym)


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
    perimeter_positions = [(0,0)]
    for line in matrix:
        acronym, meters, _ = line.split()
        for _ in range(int(meters)):
            perimeter_positions.append(add_coordinates(perimeter_positions[-1], to_direction(acronym)))
    perimeter_value = len(perimeter_positions) - 1
    # total value
    area = apply_shoelace_formula(perimeter_positions)
    inner_area = find_number_of_inner_points_with_pick_theorem(area, perimeter_value)

    return perimeter_value + inner_area


if __name__ == "__main__":
    print(part_one(parsed_input()))
