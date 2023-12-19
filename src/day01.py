from typing import List


def to_calibration(document: str):
    numbers = [int(s) for s in document if s.isdigit()]

    return numbers[0] * 10 + numbers[-1]


def to_digit_numbers_only(document: str):
    tokens = {
        "one": "1",
        "two": "2",
        "three": "3",
        "four": "4",
        "five": "5",
        "six": "6",
        "seven": "7",
        "eight": "8",
        "nine": "9",
    }

    def tokenize(document_: str) -> List[str]:
        if len(document_) == 1:
            return [document_]

        k = 1
        while k < len(document_):
            substring = document_[:k]
            if substring in tokens.keys():
                return [substring] + tokenize(document_[k:])
            k += 1

        substring = document_[:k]
        if substring in tokens.keys():
            return [substring]
        k += 1
        return [document_[0]] + tokenize(document_[1:])

    def translate(token: str) -> str:
        if token in tokens.keys():
            return tokens[token]
        else:
            return token

    return "".join(translate(token) for token in tokenize(document))


def _parse():
    with open("input.dat", "r") as data:
        return [line.strip() for line in data.readlines()]


def part_one():
    return sum(to_calibration(document) for document in _parse())


def part_two():
    return sum(to_calibration(to_digit_numbers_only(document)) for document in _parse())


if __name__ == "__main__":
    print(part_one(), part_two())
