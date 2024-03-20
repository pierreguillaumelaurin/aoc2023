from heapq import heappop, heappush
from typing import List

from src.utils import benchmark


def parsed_input():
    with open("./input.dat", "r") as data:
        return [line.strip() for line in data.readlines()]


@benchmark
def part_one(matrix: List[str]):
    seen = set()
    priority_queue = [(0, 0, 0, 0, 0, 0)]
    directions = ((0, 1), (0, -1), (1, 0), (-1, 0))
    while priority_queue:
        heat_loss, x, y, x_direction, y_direction, straight_moves = heappop(
            priority_queue
        )

        if (x, y) == (len(matrix) - 1, len(matrix[0]) - 1):
            return heat_loss

        if (x, y, x_direction, y_direction, straight_moves) in seen:
            continue
        seen.add((x, y, x_direction, y_direction, straight_moves))

        if straight_moves < 3:
            next_x = x + x_direction
            next_y = y + y_direction
            if 0 <= next_x < len(matrix) and 0 <= next_y < len(matrix[0]):
                heappush(
                    priority_queue,
                    (
                        heat_loss + int(matrix[next_x][next_y]),
                        next_x,
                        next_y,
                        x_direction,
                        y_direction,
                        straight_moves + 1,
                    ),
                )

        for next_x_direction, next_y_direction in directions:
            if (next_x_direction, next_y_direction) != (x_direction, y_direction) and (
                next_x_direction,
                next_y_direction,
            ) != (-x_direction, -y_direction):
                next_x = x + next_x_direction
                next_y = y + next_y_direction
                if 0 <= next_x < len(matrix) and 0 <= next_y < len(matrix[0]):
                    heappush(
                        priority_queue,
                        (
                            heat_loss + int(matrix[next_x][next_y]),
                            next_x,
                            next_y,
                            next_x_direction,
                            next_y_direction,
                            1,
                        ),
                    )
    return None


@benchmark
def part_two(matrix: List[str]):
    seen = set()
    priority_queue = [(0, 0, 0, 0, 0, 0)]
    directions = ((0, 1), (0, -1), (1, 0), (-1, 0))
    while priority_queue:
        heat_loss, x, y, x_direction, y_direction, straight_moves = heappop(
            priority_queue
        )

        if (x, y) == (len(matrix) - 1, len(matrix[0]) - 1) and straight_moves >= 4:
            return heat_loss

        if (x, y, x_direction, y_direction, straight_moves) in seen:
            continue
        seen.add((x, y, x_direction, y_direction, straight_moves))

        if straight_moves < 10:
            next_x = x + x_direction
            next_y = y + y_direction
            if 0 <= next_x < len(matrix) and 0 <= next_y < len(matrix[0]):
                heappush(
                    priority_queue,
                    (
                        heat_loss + int(matrix[next_x][next_y]),
                        next_x,
                        next_y,
                        x_direction,
                        y_direction,
                        straight_moves + 1,
                    ),
                )

        if straight_moves >= 4 or (x_direction, y_direction) == (
            0,
            0,
        ):  # TODO remove 0,0
            for next_x_direction, next_y_direction in directions:
                if (next_x_direction, next_y_direction) != (
                    x_direction,
                    y_direction,
                ) and (next_x_direction, next_y_direction) != (
                    -x_direction,
                    -y_direction,
                ):
                    next_x = x + next_x_direction
                    next_y = y + next_y_direction
                    if 0 <= next_x < len(matrix) and 0 <= next_y < len(matrix[0]):
                        heappush(
                            priority_queue,
                            (
                                heat_loss + int(matrix[next_x][next_y]),
                                next_x,
                                next_y,
                                next_x_direction,
                                next_y_direction,
                                1,
                            ),
                        )
    return None


if __name__ == "__main__":
    assert part_one(parsed_input()) == 859
    print(part_one(parsed_input()))
    assert part_two(parsed_input()) == 1027
    print(part_two(parsed_input()))
