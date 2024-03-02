from functools import cache
from itertools import groupby
from typing import List, Tuple

from src.utils import benchmark


def parsed_input() -> List[Tuple[str, ...]]:
    with open("./input.dat", "r") as data:
        return [tuple(parts) for line in data.readlines() if len(parts := line.strip().split()) == 2]


class Converter:
    @staticmethod
    def to_state_symbol(number: bin):
        def to_state_symbol(digit: bin):
            match digit:
                case "0":
                    return "."
                case "1":
                    return "#"
                case _:
                    raise ValueError("invalid int:", digit)

        _number = number[2:]
        return "".join(to_state_symbol(digit) for digit in _number)

    @staticmethod
    def to_binary(state_symbol: str) -> bin:
        def to_binary(character: str):
            match character:
                case "#":
                    return "1"
                case ".":
                    return "0"
                case _:
                    raise ValueError("invalid int:", character)

        return "0b" + "".join(to_binary(character) for character in state_symbol)


def satisfies(element_count: List[int], requirements: List[int]):
    return element_count == requirements


def get_arrangements(record: str):
    @cache
    def replace_question_marks(_record: str, binary_number_for_each_indexes: str):
        result = ""
        _binary_symbols = Converter.to_state_symbol(binary_number_for_each_indexes)
        for char in _record:
            if char == "?":
                number_to_add, *rest = _binary_symbols
                result += number_to_add
                _binary_symbols = rest
            else:
                result += char

        assert len(_binary_symbols) == 0
        return result

    question_mark_indexes = [
        i for i, char in enumerate(record) if char == "?"
    ]  # TODO refactor
    question_mark_length = len(question_mark_indexes)
    binary_numbers = [
        to_binary_number(n, length=question_mark_length)
        for n in range(2**question_mark_length)
    ]  # TODO extract

    return (replace_question_marks(record, n) for n in binary_numbers)


def to_binary_number(n, length):
    return "0b" + bin(n)[2:].zfill(length)


def to_contiguous_groups_length(arrangement: str):
    return [
        sum(1 for _ in group) for label, group in groupby(arrangement) if label == "#"
    ]


@benchmark
def get_number_of_valid_arrangements(record: str, requirements: List[int]):
    return sum(
        1
        for arrangement in get_arrangements(record)
        if satisfies(to_contiguous_groups_length(arrangement), requirements)
    )


def to_int_list(str_list: List[str]):
    return [int(n) for n in str_list]


@benchmark
def part_one(lines: List[Tuple[str, ...]]):
    data = [
        (record, to_int_list(requirements.split(",")))
        for (record, requirements) in lines
    ]

    return sum(
        get_number_of_valid_arrangements(record, requirements)
        for record, requirements in data
    )


@benchmark
def part_two(lines: List[str]):
    pass


if __name__ == "__main__":
    # assert part_one(parsed_input()) == 8022
    print(part_one(parsed_input()))
