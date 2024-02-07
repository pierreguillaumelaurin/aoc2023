import re
from functools import cache, lru_cache
from math import prod
from typing import Dict, List, Tuple

from src.utils import benchmark

Race = Tuple[int, int]


def parsed_input():
    with open("./input.dat", "r") as data:
        return [line.strip() for line in data.readlines()]


def number_of_ways_to_win(race: Race):
    time, record_in_mm = race

    @cache
    def rec(race_duration_: int, time_button_pressed: int):
        if time_button_pressed == race_duration_:
            return 0
        elif to_race_result(race_duration_, time_button_pressed) > record_in_mm:
            return 1 + rec(race_duration_, time_button_pressed + 1)
        else:
            return 0 + rec(race_duration_, time_button_pressed + 1)

    return rec(time, 0)


def to_race_result(race_duration: int, time_button_pressed: int):
    return (race_duration - time_button_pressed) * time_button_pressed


@benchmark
def part_one(lines: List[str]):
    races = {
        int(time.group()): int(distance.group())
        for time, distance in zip(
            re.finditer(r"\d+", lines[0]), re.finditer(r"\d+", lines[1])
        )
    }

    number_of_winning_strategies_by_race = [
        number_of_ways_to_win(race) for race in races.items()
    ]
    return prod(number_of_winning_strategies_by_race)


@benchmark
def part_two(lines: List[str]):
    def shortest_button_hold_that_wins(race_: Race):
        time, record_in_mm = race_
        return next(
            time_button_pressed
            for time_button_pressed in range(time)
            if to_race_result(
                time, time_button_pressed
            )
            > record_in_mm
        )

    def longest_button_hold_that_wins(race_: Race):
        time, record_in_mm = race_
        return next(
            time_button_pressed
            for time_button_pressed in range(time, 0, -1)
            if to_race_result(
                time, time_button_pressed
            )
            > record_in_mm
        )

    race = next(
        (int(time.group()), int(distance.group()))
        for time, distance in zip(
            re.finditer(r"\d+", lines[0].replace(" ", "")),
            re.finditer(r"\d+", lines[1].replace(" ", "")),
        )
    )

    return (
        longest_button_hold_that_wins(race) - shortest_button_hold_that_wins(race) + 1
    )


if __name__ == "__main__":
    print(part_one(parsed_input()))
    print(part_two(parsed_input()))
