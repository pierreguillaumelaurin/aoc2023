import time
from typing import Iterable


def flatten(nested_lists: Iterable[Iterable]):
    return [element for list_ in nested_lists for element in list_]


def print_with_benchmark(func):
    start_time = time.time()
    print(func())
    end_time = time.time()
    print(f"code executed in {end_time - start_time} seconds.")
