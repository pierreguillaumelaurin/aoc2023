from src.day15.day15 import imperative_hash_algorithm, part_two

FIRST_EXAMPLE = "rn=1"

FULL_EXAMPLE = "rn=1,cm-,qp=3,cm=2,qp-,pc=4,ot=9,ab=5,pc-,pc=6,ot=7"


def test_part_one():
    assert imperative_hash_algorithm(FIRST_EXAMPLE) == 30

def test_part_two():
    assert part_two(FULL_EXAMPLE) == 145
