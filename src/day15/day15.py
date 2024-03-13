from collections import defaultdict
from functools import reduce
from typing import List, Dict

from src.utils import benchmark


def parsed_input():
    with open("./input.dat", "r") as data:
        return data.readline()

def hash_algorithm(line: str):
    def subroutine(current_value: int, char: str):
        return (current_value + ord(char)) * 17 % 256

    return sum(
        reduce(subroutine, word, 0) for word in line.split(",")
    )


class Len:
    def __init__(self, focal_length):
        self.focal_length = focal_length

    @staticmethod
    def get_box_number(label: str):
        return hash_algorithm(label)


@benchmark
def part_one(line: str):
    return hash_algorithm(line)

@benchmark
def imperative_hash_algorithm(line: str):
    result = 0
    current_value = 0
    for word in line.split(','):
        for char in word:
            current_value += ord(char)
            current_value *= 17
            current_value %= 256
        result += current_value
        current_value = 0
    return result

@benchmark
def part_two(line: str):
    state: Dict[str, List[Len]] = defaultdict(list)
    for len in line:
        if len[-1] == '-':

        else:
            pass


if __name__ == "__main__":
    print(imperative_hash_algorithm(parsed_input()))
    assert part_one(parsed_input()) == 513214
    assert imperative_hash_algorithm(parsed_input()) == 513214
    assert hash_algorithm(parsed_input()) == 513214
