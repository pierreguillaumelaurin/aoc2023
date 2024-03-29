from functools import cache
from typing import List, Tuple

from src.utils import benchmark


def parsed_input() -> List[Tuple[str, ...]]:
    with open("./input.dat", "r") as data:
        return [
            tuple(parts)
            for line in data.readlines()
            if len(parts := line.strip().split()) == 2
        ]


def to_int_tuple(str_list: List[str]):
    return tuple(int(n) for n in str_list)


@cache
def valid_arrangements_count(record: str, requirements: Tuple[int, ...]):
    def can_create_next_block(record_, requirements_):
        return (
            len(record_) >= requirements_[0]
            and "." not in record_[: requirements_[0]]
            and (len(record_) == requirements_[0] or record_[requirements_[0]] != "#")
        )

    if record == "" and requirements == ():
        return 1
    if record == "" and requirements != ():
        return 0
    if requirements == ():
        return 0 if "#" in record else 1
    if record[0] == ".":
        return valid_arrangements_count(record[1:], requirements)
    if record[0] == "#" and can_create_next_block(record, requirements):
        return valid_arrangements_count(record[requirements[0] + 1 :], requirements[1:])
    if record[0] == "#" and not can_create_next_block(record, requirements):
        return 0
    if record[0] == "?" and can_create_next_block(record, requirements):
        return valid_arrangements_count(
            record[1:], requirements
        ) + valid_arrangements_count(record[requirements[0] + 1 :], requirements[1:])
    if record[0] == "?" and not can_create_next_block(record, requirements):
        return valid_arrangements_count(record[1:], requirements)
    raise ValueError("Oops! A case was not catched:", record, requirements)


@benchmark
def part_one(lines: List[Tuple[str, ...]]):
    data = [
        (record, to_int_tuple(requirements.split(",")))
        for (record, requirements) in lines
    ]

    return sum(
        valid_arrangements_count(record, requirements) for record, requirements in data
    )


@benchmark
def part_two(lines: List[Tuple[str, ...]]):
    data = [
        ("?".join([record] * 5), to_int_tuple(requirements.split(",")) * 5)
        for (record, requirements) in lines
    ]

    return sum(
        valid_arrangements_count(record, requirements) for record, requirements in data
    )


if __name__ == "__main__":
    assert part_one(parsed_input()) == 8022
    print(part_one(parsed_input()))
    assert part_two(parsed_input()) == 4968620679637
    print(part_two(parsed_input()))
