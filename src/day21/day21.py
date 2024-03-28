from collections import deque
from typing import List

from src.coordinates import Coordinates
from src.utils import benchmark


def parsed_input():
    with open("./input.dat", "r") as data:
        return [line.strip() for line in data.readlines()]


def get_adjacent_cells(coordinates: Coordinates, matrix: List[List[str]]):
    x, y = coordinates
    adjacent_cells = ((x, y - 1), (x, y + 1), (x - 1, y), (x + 1, y))
    return [
        (r, c)
        for (r, c) in adjacent_cells
        if 0 <= r < len(matrix) and 0 <= c < len(matrix[0])
    ]


@benchmark
def part_one(matrix: List[List[str]], required_steps=64):
    starting_position = next(
        (i, j)
        for i, row in enumerate(matrix)
        for j, cell in enumerate(row)
        if cell == "S"
    )

    reachable_garden_plots = {starting_position}
    for _ in range(required_steps):
        reachable_garden_plots = {
            (x, y)
            for plot in reachable_garden_plots
            for (x, y) in get_adjacent_cells(plot, matrix)
            if matrix[x][y] != "#"
        }
    return len(reachable_garden_plots)


@benchmark
def part_two(matrix: List[List[str]]):
    required_steps = 26501365
    starting_row, starting_column = next(
        (i, j)
        for i, row in enumerate(matrix)
        for j, cell in enumerate(row)
        if cell == "S"
    )

    def fill(coords: Coordinates, starting_position):
        sr, sc = coords
        ans = set()
        seen = {(sr, sc)}
        q = deque([(sr, sc, starting_position)])

        while q:
            r, c, s = q.popleft()

            if s % 2 == 0:
                ans.add((r, c))
            if s == 0:
                continue

            for nr, nc in [(r + 1, c), (r - 1, c), (r, c + 1), (r, c - 1)]:
                if (
                    nr < 0
                    or nr >= len(matrix)
                    or nc < 0
                    or nc >= len(matrix[0])
                    or matrix[nr][nc] == "#"
                    or (nr, nc) in seen
                ):
                    continue
                seen.add((nr, nc))
                q.append((nr, nc, s - 1))

        return len(ans)

    size = len(matrix)

    assert size == len(matrix[0])
    assert starting_row, starting_column == size / 2
    assert required_steps % size == size // 2

    matrix_width = required_steps // size - 1
    odd_matrices_points = (matrix_width // 2 * 2 + 1) ** 2
    even_matrices_points = ((matrix_width + 1) // 2 * 2) ** 2

    odd_matrices = fill((starting_row, starting_column), size * 2 + 1)
    even_matrices = fill((starting_row, starting_column), size * 2)

    corner_t = fill((size - 1, starting_column), size - 1)
    corner_r = fill((starting_row, 0), size - 1)
    corner_b = fill((0, starting_column), size - 1)
    corner_l = fill((starting_row, size - 1), size - 1)

    small_tr = fill((size - 1, 0), size // 2 - 1)
    small_tl = fill((size - 1, size - 1), size // 2 - 1)
    small_br = fill((0, 0), size // 2 - 1)
    small_bl = fill((0, size - 1), size // 2 - 1)

    large_tr = fill((size - 1, 0), size * 3 // 2 - 1)
    large_tl = fill((size - 1, size - 1), size * 3 // 2 - 1)
    large_br = fill((0, 0), size * 3 // 2 - 1)
    large_bl = fill((0, size - 1), size * 3 // 2 - 1)

    return (
        odd_matrices * odd_matrices_points
        + even_matrices * even_matrices_points
        + corner_t
        + corner_r
        + corner_b
        + corner_l
        + (matrix_width + 1) * (small_tr + small_tl + small_br + small_bl)
        + matrix_width * (large_tr + large_tl + large_br + large_bl)
    )


if __name__ == "__main__":
    assert part_one(parsed_input()) == 3737
    print(part_two(parsed_input()))
    assert part_two(parsed_input()) == 625382480005896
