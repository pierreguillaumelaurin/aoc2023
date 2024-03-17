from collections import defaultdict
from functools import reduce
from typing import Dict, List

from src.utils import benchmark


def parsed_input():
    with open("./input.dat", "r") as data:
        return data.readline()


def hash_algorithm(line: str):  # TODO hide implementation
    def subroutine(current_value: int, char: str):
        return (current_value + ord(char)) * 17 % 256

    return sum(reduce(subroutine, word, 0) for word in line.split(","))


class Lens:
    def __init__(self, label, focal_length):
        self.label = label
        self.focal_length = focal_length

    def __eq__(self, other):  # TODO remove or test
        if isinstance(other, Lens):
            return self.label == other.label
        return False

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
    for word in line.split(","):
        for char in word:
            current_value += ord(char)
            current_value *= 17
            current_value %= 256
        result += current_value
        current_value = 0
    return result


@benchmark
def part_two(line: str):
    boxes: Dict[int, List[Lens]] = defaultdict(list)
    # add lens
    for lens in line.split(","):
        if lens[-1] == "-":
            label = lens[:-1]
            boxes[hash_algorithm(label)] = [
                lens for lens in boxes[hash_algorithm(label)] if lens.label != label
            ]
        else:
            label, focal_length = lens.split("=")
            new = Lens(label, int(focal_length))
            box = boxes[hash_algorithm(new.label)]  # TODO reuse
            boxes[hash_algorithm(new.label)] = box = [
                new if lens.label == new.label else lens for lens in box
            ]
            if new not in box:
                box.append(new)
    # get total focusing power
    return sum(
        (1 + box) * (1 + lenses.index(lens)) * lens.focal_length
        for box, lenses in boxes.items()
        for lens in lenses
    )


if __name__ == "__main__":
    print(imperative_hash_algorithm(parsed_input()))
    assert part_one(parsed_input()) == 513214
    assert imperative_hash_algorithm(parsed_input()) == 513214  # TODO
    assert hash_algorithm(parsed_input()) == 513214

    print(part_two(parsed_input()))
    assert part_two(parsed_input()) == 258826
