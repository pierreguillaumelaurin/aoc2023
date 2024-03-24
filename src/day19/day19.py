import re
from math import prod
from typing import List, Literal, Tuple, TypedDict

from src.utils import benchmark


def parsed_input():
    with open("./input.dat", "r") as data:
        return [line.strip() for line in data.readlines()]


@benchmark
def part_one(lines: List[str]):
    class Part(TypedDict):
        x: int
        m: int
        a: int
        s: int

    def to_part(raw_part: str) -> Part:
        part = {}
        for raw_rating in raw_part.split(","):
            rating, _, *raw_number = raw_rating
            number = int("".join(raw_number))
            part[rating] = number
        return part

    raw_workflows, parts = lines[: lines.index("")], lines[lines.index("") + 1 :]
    workflows = {
        line[: line.index("{")]: line[line.index("{") + 1 : -1]
        for line in raw_workflows
    }

    def parse(part: Part, workflow_id: str):
        if workflow_id == "A":
            return sum(part.values())
        if workflow_id == "R":
            return 0
        workflow_conditions = workflows[workflow_id].split(",")
        for condition in workflow_conditions[:-1]:
            (rating, comparator, *raw_number), next_id = condition.split(":")
            number = int("".join(raw_number))

            match comparator:
                case "<":
                    if part[rating] < number:
                        return parse(part, next_id)
                case ">":
                    if part[rating] > number:
                        return parse(part, next_id)
                case _:
                    raise ValueError(
                        "Oops! A value occured which shouldn't have", comparator
                    )
        return parse(part, workflow_conditions[-1])

    return sum(parse(to_part(raw_part[1:-1]), "in") for raw_part in parts)


@benchmark
def part_two(lines: List[str]):
    class ValidRatingRanges(TypedDict):
        x: Tuple[int, int]
        m: Tuple[int, int]
        a: Tuple[int, int]
        s: Tuple[int, int]

    raw_workflows = lines[: lines.index("")]
    workflows = {
        line[: line.index("{")]: line[line.index("{") + 1 : -1]
        for line in raw_workflows
    }

    def parse(part: ValidRatingRanges, workflow_id: str):
        if workflow_id == "A":
            return prod(end - start + 1 for start, end in part.values())
        if workflow_id == "R":
            return 0
        workflow_conditions = workflows[workflow_id].split(",")
        result = 0
        filtered_part = part
        for condition in workflow_conditions[:-1]:
            (rating, comparator, *raw_number), next_id = condition.split(":")
            number = int("".join(raw_number))

            match comparator:
                case "<":
                    if part[rating][1] < number:
                        result += parse(part, next_id)
                    else:
                        next_part = {
                            **filtered_part,
                            rating: (filtered_part[rating][0], number - 1),
                        }
                        filtered_part = {
                            **filtered_part,
                            rating: (number, filtered_part[rating][1]),
                        }
                        result += parse(next_part, next_id)
                case ">":
                    if part[rating][0] > number:
                        result += parse(part, next_id)
                    else:
                        next_part = {
                            **filtered_part,
                            rating: (number + 1, filtered_part[rating][1]),
                        }
                        filtered_part = {
                            **filtered_part,
                            rating: (filtered_part[rating][0], number),
                        }
                        result += parse(next_part, next_id)
                case _:
                    raise ValueError(
                        "Oops! A value occured which shouldn't have", comparator
                    )
        result += parse(filtered_part, workflow_conditions[-1])
        return result

    possible_ratings = {"x": (1, 4000), "m": (1, 4000), "a": (1, 4000), "s": (1, 4000)}
    return parse(possible_ratings, "in")


if __name__ == "__main__":
    print(part_one(parsed_input()))
    assert part_one(parsed_input()) == 432434
    print(part_two(parsed_input()))
    assert part_two(parsed_input()) == 132557544578569
