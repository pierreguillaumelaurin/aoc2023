from typing import List, Tuple

import networkx as nx

from src.utils import benchmark


def parsed_input():
    with open("./input.dat", "r") as data:
        _parsed_input = []

        for line in data.readlines():
            k, v = line.strip().split(": ")
            _parsed_input += [(k, wire) for wire in v.split()]

        return _parsed_input


@benchmark
def part_one(edges: List[Tuple[str, str]]):
    graph = nx.Graph()
    graph.add_edges_from(edges)

    cut_value, subgroups = nx.stoer_wagner(graph)

    assert cut_value == 3

    return len(subgroups[0]) * len(subgroups[1])


if __name__ == "__main__":
    print(part_one(parsed_input()))
