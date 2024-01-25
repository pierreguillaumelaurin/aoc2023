from typing import List, Tuple
import re


def parsed_input():
    with open("./input.dat", "r") as data:
        return [line.strip() for line in data.readlines()]


def numbers_in_string(string: str) -> List[int]:
    return [int(match) for match in re.findall("\d+", string)]


def get_card_info(line) -> Tuple[int, List[int], List[int]]:
    card_number_section, winning_numbers_section, player_numbers_section = (
        numbers_in_string(substring) for substring in re.split("[:|]", line)
    )

    return card_number_section[0], winning_numbers_section, player_numbers_section


def part_one(lines: List[str]):
    def card_value(line):
        _, winning_numbers, player_numbers = get_card_info(line)
        valid_numbers = [n for n in player_numbers if n in winning_numbers]

        return 2 ** (len(valid_numbers) - 1) if len(valid_numbers) > 0 else 0

    return sum(card_value(line) for line in lines)


def part_two(lines: List[str]):
    card_numbers = (get_card_info(line)[0] for line in lines)
    instances = {n: 1 for n in card_numbers}

    for line in lines:
        card_number, winning_numbers, player_numbers = get_card_info(line)
        valid_numbers = [n for n in player_numbers if n in winning_numbers]
        for card_to_increment_number in range(
            card_number, card_number + len(valid_numbers)
        ):
            instances[card_to_increment_number + 1] += instances[card_number]

    return sum(n for n in instances.values())


if __name__ == "__main__":
    print(part_one(parsed_input()), part_two(parsed_input()))
