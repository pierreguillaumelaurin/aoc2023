import re
from collections import deque
from copy import deepcopy
from typing import Dict, Iterable, List, Tuple

from src.utils import benchmark, flatten


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


def get_dependencies(block: Brick, blocks: List[Brick]):
    deps = get_overlap(block, blocks[: blocks.index(block)])
    return [dep for dep in deps if dep[1][2] == max(dep_[1][2] for dep_ in deps)]


def is_removable(block: Brick, bricks: List[Brick]):
    blocks_above = get_overlap(block, bricks[bricks.index(block) + 1 :])
    return not any(
        len(dependencies := get_dependencies(block_above, bricks)) == 1
        and block in dependencies
        and block_above[0][2] - block[1][2] == 1
        for block_above in blocks_above
    )


def simulate_fall(blocks: List[Brick]):
    updated_blocks = sorted(blocks, key=lambda x: x[0][2])
    for i, block in enumerate(updated_blocks):
        ajusted_block = (
            (
                block[0][0],
                block[0][1],
                (
                    1
                    if len(deps := get_dependencies(block, updated_blocks)) == 0
                    else max(dep[1][2] for dep in deps) + 1
                ),
            ),
            (
                block[1][0],
                block[1][1],
                (
                    1 + block[1][2] - block[0][2]
                    if len(deps := get_dependencies(block, updated_blocks)) == 0
                    else max(dep[1][2] for dep in deps) + block[1][2] - block[0][2] + 1
                ),
            ),
        )
        updated_blocks[i] = ajusted_block

    return updated_blocks


def to_dependency_graph(blocks_after_fall: List[Brick]) -> Dict[Brick, List[Brick]]:
    dependency_graph = {block: [] for block in blocks_after_fall}

    for block in blocks_after_fall:
        for dependency in get_dependencies(block, blocks_after_fall):
            dependency_graph[dependency].append(block)
    return dependency_graph


def to_supported_by(blocks_after_fall: List[Brick]) -> Dict[Brick, List[Brick]]:
    dependency_graph = {block: [] for block in blocks_after_fall}

    for block in blocks_after_fall:
        for dependency in get_dependencies(block, blocks_after_fall):
            dependency_graph[block].append(dependency)
    return dependency_graph


@benchmark
def part_one(coordinates: List[List[int]]):
    assert all(coordinate[2] <= coordinate[5] for coordinate in coordinates)

    blocks: List[Brick] = [
        ((x1, y1, z1), (x2, y2, z2)) for x1, y1, z1, x2, y2, z2 in coordinates
    ]
    blocks_after_fall = simulate_fall(blocks)
    dependency_graph = to_dependency_graph(blocks_after_fall)
    dependency_graph_values = flatten(dependency_graph.values())

    return sum(
        1
        for block, dependent_blocks in dependency_graph.items()
        if len(dependent_blocks) == 0
        or all(dependency_graph_values.count(dep) > 1 for dep in dependent_blocks)
    )


def falling_bricks_count_on_removal(
    block: Brick,
    dependency_graph: Dict[Brick, List[Brick]],
    supported_by: Dict[Brick, List[Brick]],
):
    _supported_by = deepcopy(supported_by)
    fallen = set(block)
    seen = set()
    priority = deque([block])
    while priority:
        next_block = priority.popleft()
        next_block_deps = dependency_graph[next_block]
        for dep in next_block_deps:
            if dep not in seen and all(dep_ in fallen for dep_ in _supported_by[dep]):
                fallen.add(dep)
                priority.extend(dependency_graph[dep])
            seen.add(dep)
    return len(fallen)


@benchmark
def part_two(coordinates: List[List[int]]):
    assert all(coordinate[2] <= coordinate[5] for coordinate in coordinates)

    blocks: List[Brick] = [
        ((x1, y1, z1), (x2, y2, z2)) for x1, y1, z1, x2, y2, z2 in coordinates
    ]
    blocks_after_fall = simulate_fall(blocks)
    dependency_graph = to_dependency_graph(blocks_after_fall)
    supported_by = to_supported_by(blocks_after_fall)

    return sum(
        falling_bricks_count_on_removal(block, dependency_graph, supported_by)
        for block in dependency_graph
    )


if __name__ == "__main__":
    assert part_one(parsed_input()) == 401
    print(part_one(parsed_input()))
    print(part_two(parsed_input()))
