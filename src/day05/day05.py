import re
from typing import Dict, Iterable, List, Tuple, TypedDict


def parsed_input():
    with open("./input.dat", "r") as data:
        return [line.strip() for line in data.readlines()]


Section = Dict[int, int]


def to_section(raw: List[str]) -> Section:
    section = {}

    lines_with_values = [line for line in raw if "map" not in line]
    for line in lines_with_values:
        destination, source, range_ = [
            int(match.group()) for match in re.finditer(r"\d+", line)
        ]
        for s, d in zip(
            range(source, source + range_), range(destination, destination + range_)
        ):
            section[s] = d

    return section


def to_sections(input_: str) -> List[Section]:
    raw_sections = [
        re.split(r"\n", group.strip()) for group in re.split(r"\n\n.*map.*\n", input_)
    ]
    return [to_section(raw_section) for raw_section in raw_sections]


def traverse(sections_: List[Section], source: int):
    if not sections_:
        return source
    section = sections_[0]
    destination = section.get(source, source)
    return traverse(sections_[1:], destination)


def part_one(lines: List[str]):
    def to_seeds(line: str):
        return [int(match.group()) for match in re.finditer(r"\d+", line)]

    seeds = to_seeds(lines[0])
    sections = to_sections("\n".join(lines[1:]))

    locations = [traverse(sections, seed) for seed in seeds]

    return min(locations)


def part_two(lines: List[str]):
    def to_range_seeds(line: str):
        return [
            range(
                int(match.group().split(" ")[0]),
                int(match.group().split(" ")[0]) + int(match.group().split(" ")[1]),
            )
            for match in re.finditer(r"\d+ \d+", line)
        ]

    ranges = to_range_seeds(lines[0])
    sections = to_sections("\n".join(lines[1:]))

    locations = [traverse(sections, seed) for r in ranges for seed in r]

    return min(locations)


if __name__ == "__main__":
    assert part_one(parsed_input()) == 289863851
    print(part_one(parsed_input()), part_two(parsed_input()))
