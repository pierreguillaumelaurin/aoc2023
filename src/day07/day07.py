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


def card_count(card_set_: str) -> Dict[str, int]:
    count = defaultdict(int)
    for c in card_set_:
        count[c] += 1
    return count


def to_hand_kind_value(card_count_: Dict[str, int]) -> hex:
    base = hex(16**5)

    hand_ = [c for c in card_count_.values() if c > 0]
    match hand_:
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
        case _:
            raise Exception("hoopa loopa!", card_count_)


@benchmark
def part_one(lines: List[str]):
    non_digit_card_values = {
        "A": hex(0xE),
        "K": hex(0xD),
        "Q": hex(0xC),
        "J": hex(0xB),
        "T": hex(0xA),
    }

    def to_hand_value(non_digit_values: NonDigitCardValues, card_set: str) -> hex:
        result = hex(0)
        for card in card_set:
            result = add(multiply(result, hex(0x10)), to_hex(non_digit_values, card))
        return add(to_hand_kind_value(card_count(card_set)), result)

    hands = [tuple(line.split(" ")) for line in lines]
    hand_values = [
        (to_hand_value(non_digit_card_values, card_set), int(bid)) for card_set, bid in hands
    ]
    winnings = [int(bid) * (i + 1) for (i, (_, bid)) in enumerate(sorted_(hand_values))]
    return sum(winnings)


@benchmark
def part_two(lines: List[str]):
    non_digit_card_values = {
        "A": hex(0xE),
        "K": hex(0xD),
        "Q": hex(0xC),
        "T": hex(0xA),
        "J": hex(0x1),
    }

    def joker_ajusted_hand(card_count_: Dict[str, int]):
        def card_count_or_zero_for_j(key: str):
            return 0 if key == "J" else card_count_[key]

        max_key = max(card_count_, key=card_count_or_zero_for_j)
        if "J" in card_count_.keys() and max_key != "J":
            return {
                **card_count_,
                max_key: card_count_[max_key] + card_count_["J"],
                "J": 0,
            }
        else:
            return card_count_

    def to_hand_value(non_digit_values: NonDigitCardValues, card_set: str) -> hex:
        result = hex(0)
        card_count_ = joker_ajusted_hand(card_count(card_set))
        for card in card_set:
            result = add(multiply(result, hex(0x10)), to_hex(non_digit_values, card))
        return add(to_hand_kind_value(card_count_), result)

    hands = [tuple(line.split(" ")) for line in lines]

    hand_values = [
        (to_hand_value(non_digit_card_values, card_set), int(bid)) for card_set, bid in hands
    ]
    winnings = [int(bid) * (i + 1) for (i, (_, bid)) in enumerate(sorted_(hand_values))]
    return sum(winnings)


if __name__ == "__main__":
    assert part_one(parsed_input()) == 246795406
    assert part_two(parsed_input()) == 249356515
    print(part_one(parsed_input()))
    print(part_two(parsed_input()))
