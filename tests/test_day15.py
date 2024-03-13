from src.day15.day15 import imperative_hash_algorithm

FIRST_EXAMPLE = "rn=1"

def test_part_one():
    assert imperative_hash_algorithm(FIRST_EXAMPLE) == 30