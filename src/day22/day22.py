import re
from typing import Dict, Iterable, List, Tuple

from src.utils import benchmark


def parsed_input():
    with open("./input.dat", "r") as data:
        return [
            list(map(int, re.split(r"[,~]", line.strip()))) for line in data.readlines()
        ]


Brick = Tuple[Tuple[int, int, int], Tuple[int, int, int]]


def get_overlap(block: Brick, blocks: Iterable[Brick]):
    candidates: Dict[Brick, Tuple[range, range]] = {
        other_block: (
            range(
                max(block[0][0], other_block[0][0]),
                min(block[-1][0], other_block[-1][0]) + 1,
            ),
            range(
                max(block[0][1], other_block[0][1]),
                min(block[-1][1], other_block[-1][1]) + 1,
            ),
        )
        for other_block in blocks
    }
    return [
        key
        for key, (x_overlap, y_overlap) in candidates.items()
        if len(x_overlap) > 0 and len(y_overlap) > 0
    ]


def has_overlap_above(block: Brick, blocks: List[Brick]):
    return len(get_overlap(block, blocks[blocks.index(block) + 1:])) > 0


def get_dependencies(block: Brick, blocks: List[Brick]):
    deps = get_overlap(block, blocks[: blocks.index(block)])
    return [
        dep
        for dep in deps
        if dep[1][2] == max(dep_[1][2] for dep_ in deps)
    ]


def is_removable(block: Brick, bricks: List[Brick]):
    blocks_above = get_overlap(block, bricks[bricks.index(block) + 1:])
    return not any(
        len(dependencies := get_dependencies(block_above, bricks)) == 1
        and block in dependencies
        and block_above[0][2] - block[1][2] == 1
        for block_above in blocks_above
    )


def falling_bricks_count_on_removal(block: Brick, bricks: List[Brick]):
    blocks_above = get_overlap(block, bricks[bricks.index(block) + 1:])
    immediate_falling_bricks = [
        block_above
        for block_above in blocks_above
        if len(dependencies := get_dependencies(block_above, bricks)) == 1
           and block in dependencies
           and block_above[0][2] - block[1][2] == 1
    ]

    return len(immediate_falling_bricks) + sum(
        falling_bricks_count_on_removal(falling_brick, bricks) for falling_brick in immediate_falling_bricks)


def simulate_fall(sorted_blocks: List[Brick]):
    for i, block in enumerate(sorted_blocks):
        ajusted_block = ((block[0][0], block[0][1], (
            1 if len(deps := get_dependencies(block, sorted_blocks)) == 0 else max(dep[1][2] for dep in deps) + 1)),
                         (block[1][0], block[1][1], (1 + block[1][2] - block[0][2] if len(
                             deps := get_dependencies(block, sorted_blocks)) == 0 else max(dep[1][2] for dep in deps) +
                                                                                       block[1][2] - block[0][2] + 1)))
        sorted_blocks[i] = ajusted_block

    return sorted_blocks


@benchmark
def part_one(coordinates: List[List[int]]):
    assert all(coordinate[2] <= coordinate[5] for coordinate in coordinates)

    blocks: List[Brick] = [
        ((x1, y1, z1), (x2, y2, z2)) for x1, y1, z1, x2, y2, z2 in coordinates
    ]
    sorted_blocks = sorted(blocks, key=lambda x: x[0][2])  # TODO add in simulate fall
    blocks_after_fall = simulate_fall(sorted_blocks)
    return sum(is_removable(block, blocks_after_fall) for block in blocks_after_fall)


@benchmark
def part_two(coordinates: List[List[int]]):
    assert all(coordinate[2] <= coordinate[5] for coordinate in coordinates)

    blocks: List[Brick] = [
        ((x1, y1, z1), (x2, y2, z2)) for x1, y1, z1, x2, y2, z2 in coordinates
    ]
    sorted_blocks = sorted(blocks, key=lambda x: x[0][2])  # TODO add in simulate fall
    blocks_after_fall = simulate_fall(sorted_blocks)
    return sum(falling_bricks_count_on_removal(block, blocks_after_fall) for block in blocks_after_fall)


if __name__ == "__main__":
    assert part_one(parsed_input()) == 401
    print(part_one(parsed_input()))
