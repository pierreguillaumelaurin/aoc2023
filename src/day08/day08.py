import re
from math import lcm
from typing import Dict, List, Tuple

from src.utils import benchmark


def parsed_input():
    with open("./input.dat", "r") as data:
        return [line.strip() for line in data.readlines()]


def to_node(raw_node: str):
    return [node.group() for node in re.finditer(r"\w+", raw_node)]


def to_network(raw_network: List[str]):
    network = {}
    for raw_node in raw_network:
        source, first_destination, second_destination = to_node(raw_node)
        network[source] = (first_destination, second_destination)
    return network


def count_for_key(
    instructions: str,
    network: Dict[str, Tuple[str, str]],
    starting_key: str,
    ending_key: str,
):
    count = 0
    current_key = starting_key
    while re.match(ending_key, current_key) is None:
        instruction = instructions[count % len(instructions)]
        match instruction:
            case "L":
                current_key = network[current_key][0]
            case "R":
                current_key = network[current_key][1]
            case "_":
                raise Exception("oops", instruction)
        count += 1

    return count


@benchmark
def part_one(lines: List[str]):
    instructions, _, *raw_network = lines
    network = to_network(raw_network)

    return count_for_key(instructions, network, starting_key="AAA", ending_key="ZZZ")


@benchmark
def part_two(lines: List[str]):
    instructions, _, *raw_network = lines
    network = to_network(raw_network)

    current_keys = [
        line.split(" ")[0] for line in raw_network if line.split(" ")[0][-1] == "A"
    ]
    count_for_current_keys = [
        count_for_key(instructions, network, starting_key=key, ending_key=r"\w\wZ")
        for key in current_keys
    ]

    return lcm(*count_for_current_keys)


if __name__ == "__main__":
    assert part_one(parsed_input()) == 20569
    assert part_two(parsed_input()) == 21366921060721
    print(part_one(parsed_input()))
    print(part_two(parsed_input()))
