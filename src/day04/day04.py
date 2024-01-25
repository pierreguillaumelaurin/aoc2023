from typing import List
import re


def parsed_input():
    with open("input.dat", "r") as data:
        return [line.strip() for line in data.readlines()]


def part_one(lines: List[str]):
    def numbers_in_string(string: str) -> List[int]:
        return [int(match) for match in re.findall("\d+", string)]

    def card_value(line):
        _, winning_numbers, player_numbers = (
            numbers_in_string(substring) for substring in re.split("[:|]", line)
        )
        valid_numbers = [n for n in player_numbers if n in winning_numbers]

        return 2 ** (len(valid_numbers) - 1) if len(valid_numbers) > 0 else 0

    return sum(card_value(line) for line in lines)


def part_two(matrix: List[str]):
    pass


if __name__ == "__main__":
    print(part_one(parsed_input()), part_two(parsed_input()))
