from src.day20.day20 import part_one, ModuleType


def test_part_one_should_set_communication_order_correctly():
    result = part_one(
        ["broadcaster -> a, b, c", "%a -> b", "%b -> c", "%c -> inv", "&inv -> a"]
    )

    assert result == [
        ("button", "broadcaster"),
        ("broadcaster", "a"),
        ("broadcaster", "b"),
        ("broadcaster", "c"),
        ("%a", "b"),
        ("%b", "c"),
        ("%c", "inv"),
        ("&inv", "a"),
    ]


def test_first_example():
    result = part_one(["broadcaster -> a, b, c", "%a -> b", "%b -> c", "%c -> inv", "&inv -> a"])

    assert result == 32000000

    # assert result == [
    #     "LOW",
    #     "LOW",
    #     "LOW",
    #     "LOW",
    #     "HIGH",
    #     "HIGH",
    #     "HIGH",
    #     "LOW",
    #     "LOW",
    #     "LOW",
    #     "LOW",
    #     "HIGH",
    # ]
