from typing import Iterable


def flatten(nested_lists: Iterable[Iterable]):
    return [element for list_ in nested_lists for element in list_]
