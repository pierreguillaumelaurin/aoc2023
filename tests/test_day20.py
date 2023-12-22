from src.day20.day20 import part_one


def test_it_should_proceed_pulses_in_correct_order():
    result = part_one(
        ["broadcaster -> a, b, c", "%a -> b", "%b -> c", "%c -> inv", "&inv -> a"]
    )

    assert result == [
        "LOW",
        "LOW",
        "LOW",
        "LOW",
        "HIGH",
        "HIGH",
        "HIGH",
        "LOW",
        "LOW",
        "LOW",
        "LOW",
        "HIGH",
    ]
