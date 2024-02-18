from collections import deque
from typing import Deque, List

from src.utils import benchmark


def parsed_input():
    with open("./input.dat", "r") as data:
        return [line.strip() for line in data.readlines()]


def to_differences(numbers: List[Deque[int]]):
    while any(n != 0 for n in numbers[-1]):
        last = numbers[-1]
        differences = deque(last[i + 1] - last[i] for i in range(len(last) - 1))
        numbers.append(differences)
    return numbers


def with_added_values_right(differences: List[Deque[int]]):
    while len(differences) > 1:
        last = differences.pop()
        differences[-1].append(last[-1] + differences[-1][-1])
    return differences.pop()


def with_added_values_left(differences: List[Deque[int]]):
    while len(differences) > 1:
        last = differences.pop()
        differences[-1].appendleft(differences[-1][0] - last[0])
    return differences.pop()


@benchmark
def part_one(lines: List[str]):
    values = [deque(int(s) for s in line.split(" ")) for line in lines]

    return sum(
        with_added_values_right(to_differences([value])).pop() for value in values
    )


@benchmark
def part_two(lines: List[str]):
    values = [deque(int(s) for s in line.split(" ")) for line in lines]

    return sum(
        with_added_values_left(to_differences([value])).popleft() for value in values
    )


if __name__ == "__main__":
    assert part_one(parsed_input()) == 1884768153

    print(part_one(parsed_input()))
    print(part_two(parsed_input()))
