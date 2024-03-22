from src.day19.day19 import part_one, to_python_function

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
        == "def x(x,m,a,s):\n    if a<2006:\n        return qkq(w)\n    if m>2090:\n        return A(w)\n    return rfg(w)"
    )


def test_part_one():
    assert part_one(EXAMPLE) == 19114
