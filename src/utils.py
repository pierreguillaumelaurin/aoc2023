import functools
import time
from typing import Iterable


def flatten(nested_lists: Iterable[Iterable]):
    return [element for list_ in nested_lists for element in list_]


def benchmark(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.perf_counter()  # 1
        value = func(*args, **kwargs)
        end_time = time.perf_counter()  # 2
        print(f"{func.__name__!r} executed in {end_time - start_time} seconds.")
        return value

    return wrapper
