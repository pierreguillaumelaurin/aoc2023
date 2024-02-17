import re
from typing import List

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


@benchmark
def part_one(lines: List[str]):
    instructions, _, *raw_network = lines
    network = to_network(raw_network)

    count = 0
    current_key = "AAA"
    while current_key != "ZZZ":
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
def part_two(lines: List[str]):
    instructions, _, *raw_network = lines
    network = to_network(raw_network)

    count = 0
    current_keys = [line.split(" ")[0] for line in raw_network if line.split(" ")[0][-1] == "A"]
    print(current_keys)


if __name__ == "__main__":
    print(part_one(parsed_input()))
    print(part_two(parsed_input()))
