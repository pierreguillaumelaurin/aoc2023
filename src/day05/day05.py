import re
from typing import Iterable, List, Tuple, TypedDict


def parsed_input():
    with open("./input.dat", "r") as data:
        return [line.strip() for line in data.readlines()]


# TODO delete
class Map(dict):
    def __missing__(self, key):
        return key


class Section(TypedDict):
    destinations: Tuple[int]
    sources: Tuple[int]
    ranges: Tuple[int]


def to_section(raw: List[str]) -> Section:
    section = {"sources": [], "destinations": [], "ranges": []}

    lines_with_values = [line for line in raw if "map" not in line]
    for line in lines_with_values:
        destination, source, range_ = [
            int(match.group()) for match in re.finditer(r"\d+", line)
        ]
        section["destinations"].append(destination)
        section["sources"].append(source)
        section["ranges"].append(range_)

    return Section(**section)


def to_sections(input_: str) -> List[Section]:
    raw_sections = [
        re.split(r"\n", group.strip()) for group in re.split(r"\n\n.*map.*\n", input_)
    ]
    return [to_section(raw_section) for raw_section in raw_sections]


# TODO delete
def to_map(section: Section) -> Map:
    map_ = Map()

    for destination, source, range_ in zip(
        section["destinations"], section["sources"], section["ranges"]
    ):
        for k, v in zip(
            range(source, source + range_), range(destination, destination + range_)
        ):
            map_[k] = v

    return map_


def traverse(sections_: List[Section], source: int):
    if not sections_:
        return source
    section = sections_[0]
    destination = get_destination(section, source)
    return traverse(sections_[1:], destination)


def get_destination(section: Section, source: int):
    def to_ranges(elements: Iterable[int], ranges_: Iterable[int]):
        return [
            range(element, element + range_)
            for element, range_ in zip(elements, ranges_)
        ]

    if any(
        source in range_ for range_ in to_ranges(section["sources"], section["ranges"])
    ):
        ranges = to_ranges(section["sources"], section["ranges"])
        range_index = [
            index
            for index, range_ in enumerate(
                to_ranges(section["sources"], section["ranges"])
            )
            if source in range_
        ][0]
        range_ = ranges[range_index]
        index_in_range = source - range_.start
        destination = section["destinations"][range_index] + index_in_range
    else:
        destination = source
    return destination


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
