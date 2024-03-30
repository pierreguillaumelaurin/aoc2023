from typing import List, Tuple, TypedDict

import sympy

from src.utils import benchmark


class Hailstone:
    def __init__(self, position, velocity):
        sx, sy, sz = position
        vx, vy, vz = velocity
        self.position = sx, sy, sz
        self.velocity = vx, vy, vz
        self.a = vy
        self.b = -vx
        self.c = vy * sx - vx * sy

    def __repr__(self):
        return f"Hailstone standard form: a={self.a}, b={self.b}, c={self.c}"


def parsed_input():
    with open("./input.dat", "r") as data:
        _parsed_input = []

        for line in data.readlines():
            position, velocity = line.strip().split(" @ ")
            _parsed_input.append(
                Hailstone(
                    **{
                        "position": map(int, position.split(", ")),
                        "velocity": map(int, velocity.split(", ")),
                    }
                )
            )

        return _parsed_input


@benchmark
def part_one(
    hailstones: List[Hailstone],
    lower_bound=200000000000000,
    higher_bound=400000000000000,
):
    total = 0
    for i, first_hailstone in enumerate(hailstones):
        for second_hailstone in hailstones[:i]:
            if (
                first_hailstone.a * second_hailstone.b
                == first_hailstone.b * second_hailstone.a
            ):  # if they are parallel
                continue
            intersection_x = (
                first_hailstone.c * second_hailstone.b
                - second_hailstone.c * first_hailstone.b
            ) / (
                first_hailstone.a * second_hailstone.b
                - second_hailstone.a * first_hailstone.b
            )
            intersection_y = (
                second_hailstone.c * first_hailstone.a
                - first_hailstone.c * second_hailstone.a
            ) / (
                first_hailstone.a * second_hailstone.b
                - second_hailstone.a * first_hailstone.b
            )
            if (
                lower_bound <= intersection_x <= higher_bound
                and lower_bound <= intersection_y <= higher_bound
            ):
                if all(
                    (intersection_x - hs.position[0]) * hs.velocity[0] >= 0
                    and (intersection_y - hs.position[1]) * hs.velocity[1] >= 0
                    for hs in (first_hailstone, second_hailstone)
                ):  # if value in future
                    total += 1
    return total


@benchmark
def part_two(hailstones: List[Hailstone]):
    equations = []
    answers = []
    xr, yr, zr, vxr, vyr, vzr = sympy.symbols("xr, yr, zr, vxr, vyr, vzr")

    for i, hailstone in enumerate(hailstones):
        sx, sy, sz = hailstone.position
        vx, vy, vz = hailstone.velocity
        equations.append((xr - sx) * (vy - vyr) - (yr - sy) * (vx - vxr))
        equations.append((yr - sy) * (vz - vzr) - (zr - sz) * (vy - vyr))
        if i < 2:
            continue
        answers = [
            collision
            for collision in sympy.solve(equations)
            if all(x % 1 == 0 for x in collision.values())
        ]

        if len(answers) == 1:
            break
    answer = answers[0]

    return answer[xr] + answer[yr] + answer[zr]


if __name__ == "__main__":
    print(part_one(parsed_input()))
    assert part_one(parsed_input()) == 12938
    print(part_two(parsed_input()))
    assert part_two(parsed_input()) == 976976197397181
