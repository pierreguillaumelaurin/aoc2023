import re
from typing import Dict, Iterable, List

Section = Dict[range, range]


def parsed_input():
    with open("./input.dat", "r") as data:
        return [line.strip() for line in data.readlines()]


def part_of(candidate: range, ranges: Iterable[range]):
    return next(
        r for r in ranges if r.start <= candidate.start and r.stop >= candidate.stop
    )


def distincts(seed: range, keys: Iterable[range]) -> List[range]:
    candidates = [seed]
    result = []
    while len(candidates) > 0:
        candidate = candidates.pop()
        matched = False
        for key in keys:
            left_overflow = candidate.start < key.start
            right_overflow = candidate.stop > key.stop

            if len(overlap(candidate, [key])) > 0:
                matched = True
                match left_overflow, right_overflow:
                    case True, True:
                        candidates.append(range(candidate.start, key.start))
                        candidates.append(range(key.stop, candidate.stop))
                    case True, False:
                        candidates.append(range(candidate.start, key.start))
                    case False, True:
                        candidates.append(range(key.stop, candidate.stop))
                    case False, False:
                        pass
        if matched is False:
            result.append(candidate)
            break
        matched = False

    return result


def overlap(seed: range, keys: Iterable[range]):
    candidates = [range(max(seed[0], key[0]), min(seed[-1], key[-1]) + 1) for key in keys]
    return [candidate for candidate in candidates if len(candidate) > 0]



def to_section(raw: List[str]) -> Section:
    section = {}

    lines_with_values = [line for line in raw if "map" not in line]
    for line in lines_with_values:
        destination, source, range_ = [
            int(match.group()) for match in re.finditer(r"\d+", line)
        ]
        section[range(source, source + range_)] = range(
            destination, destination + range_
        )

    return section


def to_sections(input_: str) -> List[Section]:
    raw_sections = [
        re.split(r"\n", group.strip()) for group in re.split(r"\n\n.*map.*\n", input_)
    ]
    return [to_section(raw_section) for raw_section in raw_sections]


def traverse(sections_: List[Section], seeds: List[range]) -> List[range]:
    def get_destination(section_: Section, seeds_: List[range]):
        overlaps = []
        distincts_ = []
        for seed in seeds_:
            seed_overlaps = overlap(seed, section_.keys())
            overlaps += seed_overlaps
            distincts_ += distincts(seed, section.keys())
            if not len(seed_overlaps):
                distincts_ += [seed]
        overlaps_keys = [part_of(o, section_.keys()) for o in overlaps]

        return [
            range(
                section_[key][o.start - key.start],
                section_[key][o.stop - key.start - 1] + 1,
            )
            for o, key in zip(overlaps, overlaps_keys)
        ] + distincts_

    if not sections_:
        return seeds
    section = sections_[0]
    destination = get_destination(section, seeds)
    return traverse(sections_[1:], destination)


def part_one(lines: List[str]):
    def to_seeds(line: str):
        return [
            range(int(match.group()), int(match.group()) + 1)
            for match in re.finditer(r"\d+", line)
        ]

    seeds = to_seeds(lines[0])
    sections = to_sections("\n".join(lines[1:]))

    locations = traverse(sections, seeds)

    return min(location.start for location in locations)


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

    locations = traverse(sections, ranges)

    return min(location.start for location in locations)


if __name__ == "__main__":
    # assert part_one(parsed_input()) == 289863851
    assert part_two(parsed_input()) > 36040106
    print(part_one(parsed_input()), part_two(parsed_input()))
