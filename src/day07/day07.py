from collections import defaultdict
from typing import Dict, List, Tuple, TypedDict

from src.utils import benchmark


def parsed_input():
    with open("./input.dat", "r") as data:
        return [line.strip() for line in data.readlines()]


def add(left_hex: hex, right_hex: hex):
    return hex(int(left_hex, 16) + int(right_hex, 16))


def multiply(left_hex: hex, right_hex: hex):
    return hex(int(left_hex, 16) * int(right_hex, 16))


def sorted_(hex_array: List[Tuple[hex, int]]):
    return sorted((int(h, 16), bid) for h, bid in hex_array)


class NonDigitCardValues(TypedDict):
    A: str
    K: str
    Q: str
    J: str
    T: str


def to_hex(non_digit_values: NonDigitCardValues, card: str) -> hex:
    return non_digit_values[card] if card in non_digit_values.keys() else hex(int(card))


def to_value(non_digit_values: NonDigitCardValues, card_set: str) -> hex:

    def card_count(card_set_: str) -> Dict[str, int]:
        count = defaultdict(int)
        for c in card_set_:
            count[c] += 1
        return count

    def to_hand_kind_value(card_set_: str) -> hex:
        base = hex(16**5)
        match card_count(card_set_).values():
            case c if len(c) == 1:
                return multiply(hex(7), base)
            case c if 4 in c:
                return multiply(hex(6), base)
            case c if 3 in c and len(c) == 2:
                return multiply(hex(5), base)
            case c if 3 in c and len(c) == 3:
                return multiply(hex(4), base)
            case c if 2 in c and len(c) == 3:
                return multiply(hex(3), base)
            case c if 2 in c and len(c) == 4:
                return multiply(hex(2), base)
            case c if len(c) == 5:
                return multiply(hex(1), base)

    result = hex(0)
    for card in card_set:
        result = add(multiply(result, hex(0x10)), to_hex(non_digit_values, card))
    return add(to_hand_kind_value(card_set), result)


@benchmark
def part_one(lines: List[str]):
    non_digit_card_values = {
        "A": hex(0xE),
        "K": hex(0xD),
        "Q": hex(0xC),
        "J": hex(0xB),
        "T": hex(0xA),
    }

    hands = [tuple(line.split(" ")) for line in lines]
    hand_values = [(to_value(non_digit_card_values, card_set), int(bid)) for card_set, bid in hands]
    winnings = [int(bid) * (i + 1) for (i, (_, bid)) in enumerate(sorted_(hand_values))]
    return sum(winnings)


@benchmark
def part_two(lines: List[str]):
    pass


if __name__ == "__main__":
    assert part_one(parsed_input()) == 246795406
    print(part_one(parsed_input()))
