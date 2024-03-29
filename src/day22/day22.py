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
    return len(get_overlap(block, blocks[blocks.index(block) + 1 :])) > 0


def get_dependencies(block: Brick, matrix: List[Brick]):
    deps = get_overlap(block, matrix[: matrix.index(block)])
    return [
        dep
        for dep in deps
        if not has_overlap_above(dep, deps) and dep[1][2] == max(dep[1][2])
    ]


def is_removable(block: Brick, matrix: List[Brick]):
    blocks_above = get_overlap(block, matrix[matrix.index(block) + 1 :])
    return not any(
        len(dependencies := get_dependencies(candidate, matrix)) == 1
        and block in dependencies
        for candidate in blocks_above
    )


@benchmark
def part_one(coordinates: List[List[int]]):
    assert all(coordinate[2] <= coordinate[5] for coordinate in coordinates)

    blocks: List[Brick] = [
        ((x1, y1, z1), (x2, y2, z2)) for x1, y1, z1, x2, y2, z2 in coordinates
    ]
    sorted_blocks = sorted(blocks, key=lambda x: x[0][2])
    return sum(is_removable(block, sorted_blocks) for block in sorted_blocks)


if __name__ == "__main__":
    print(part_one(parsed_input()))
