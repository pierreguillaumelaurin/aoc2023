from enum import Enum
from typing import Dict, List, TypedDict

from src.utils import benchmark


def parsed_input():
    with open("input.dat", "r") as data:
        return [line.strip() for line in data.readlines()]


class Game(TypedDict):
    number: int
    sets: List[Dict[str, int]]


def to_game(line: str) -> Game:
    def to_set(raw_set: str) -> Dict[str, int]:
        return {
            k.strip(): int(v.strip())
            for draft in raw_set.split(", ")
            for (v, k) in [draft.strip().split(" ")]
        }

    left, right = line.split(": ")

    return {
        "number": int(left[5:]),
        "sets": [to_set(raw_set) for raw_set in right.split(";")],
    }


@benchmark
def part_one(input_):
    def set_possible(game_set: Dict[str, int]) -> bool:
        maximum_numbers = {"red": 12, "green": 13, "blue": 14}
        return all(maximum_numbers[k] >= game_set[k] for k in game_set.keys())

    def game_possible(sets: List[Dict[str, int]]):
        return all(set_possible(game_set) for game_set in sets)

    games = [to_game(line) for line in input_]

    return sum(game["number"] for game in games if game_possible(game["sets"]))


@benchmark
def part_two(input_):
    def to_power(game: Game) -> int:
        return (
            max(v for game_set in game["sets"] for k, v in game_set.items() if k == "red")
            * max(v for game_set in game["sets"] for k, v in game_set.items() if k == "green")
            * max(v for game_set in game["sets"] for k, v in game_set.items() if k == "blue")
        )

    games = [to_game(line) for line in input_]

    return sum(to_power(game) for game in games)


if __name__ == "__main__":
    assert part_one(parsed_input()) == 1931
    assert part_two(parsed_input()) == 83105
    print(part_one(parsed_input()), part_two(parsed_input()))
