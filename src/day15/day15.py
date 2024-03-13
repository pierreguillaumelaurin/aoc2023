from src.utils import benchmark


def parsed_input():
    with open("./input.dat", "r") as data:
        return data.readline()


@benchmark
def part_one(line: str):
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
    pass

if __name__ == "__main__":
    assert part_one(parsed_input()) == 513214
    print(part_one(parsed_input()))