import time
from typing import Iterable


def flatten(nested_lists: Iterable[Iterable]):
    return [element for list_ in nested_lists for element in list_]


def print_with_benchmark(func, input_):
    start_time = time.time()
    print(func(input_))
    end_time = time.time()
    print(f"code executed in {end_time - start_time} seconds.")
