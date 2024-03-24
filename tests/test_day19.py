from src.day19.day19 import part_one, part_two
from src.day19.day19_part_one_alternate_solution import (
    part_one_alternate,
    to_python_function,
)

EXAMPLE = [
    "px{a<2006:qkq,m>2090:A,rfg}",
    "pv{a>1716:R,A}",
    "lnx{m>1548:A,A}",
    "rfg{s<537:gd,x>2440:R,A}",
    "qs{s>3448:A,lnx}",
    "qkq{x<1416:A,crn}",
    "crn{x>2662:A,R}",
    "in{s<1351:px,qqz}",
    "qqz{s>2770:qs,m<1801:hdj,R}",
    "gd{a>3333:R,R}",
    "hdj{m>838:A,pv}",
    "",
    "{x=787,m=2655,a=1222,s=2876}",
    "{x=1679,m=44,a=2067,s=496}",
    "{x=2036,m=264,a=79,s=2244}",
    "{x=2461,m=1339,a=466,s=291}",
    "{x=2127,m=1623,a=2188,s=1013}",
]


def test_to_python_function():
    assert (
        to_python_function("x{a<2006:qkq,m>2090:A,rfg}")
        == "def x(x,m,a,s):\n    if a<2006:\n        return qkq(x,m,a,s)\n    if m>2090:\n        return A(x,m,a,s)\n    return rfg(x,m,a,s)"
    )


def test_part_one():
    assert part_one(EXAMPLE) == 19114


def test_part_one_alternate():
    assert part_one_alternate(EXAMPLE) == 19114


def test_part_two():
    assert part_two(EXAMPLE) == 167409079868000
