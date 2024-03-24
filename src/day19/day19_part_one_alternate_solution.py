import re
from typing import List, Tuple

from src.utils import benchmark


def parsed_input():
    with open("./input.dat", "r") as data:
        return [line.strip() for line in data.readlines()]


def to_python_function(workflow: str):
    def parse_conditions(parts_: List[Tuple[str, ...]]) -> str:
        first_part = parts_[0]
        if len(first_part) == 1:
            return f"    return {first_part[0]}(x,m,a,s)"
        (guard, value) = first_part
        return f"    if {guard}:\n        return {value}(x,m,a,s)\n" + parse_conditions(
            parts_[1:]
        )

    name, cases = (
        workflow[: workflow.index("{")],
        workflow[workflow.index("{") + 1 : workflow.index("}")],
    )
    parts = [tuple(part for part in case.split(":")) for case in cases.split(",")]
    curated_name = "in_" if name == "in" else name
    return f"def {curated_name}(x,m,a,s):\n" + parse_conditions(parts)


def to_categories(part: str):
    return [match.group() for match in re.finditer(r"\d+", part)]


@benchmark
def part_one_alternate(lines: List[str]):
    scope = {"ratings": 0}

    exec(
        """def A(x,m,a,s):
    global ratings
    ratings += sum((x,m,a,s))""",
        scope,
    )

    exec(
        """def R(x,m,a,s):
    pass
""",
        scope,
    )

    workflows, parts = lines[: lines.index("")], lines[lines.index("") + 1 :]
    # register workflow in-memory
    for workflow in workflows:
        exec(to_python_function(workflow), scope)

    for part in parts:
        categories = to_categories(part)
        exec(f'in_({",".join(categories)})', scope)
    return scope["ratings"]


if __name__ == "__main__":
    assert part_one_alternate(parsed_input()) == 432434
    print(part_one_alternate(parsed_input()))
