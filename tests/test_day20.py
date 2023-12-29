from src.day20.day20 import (
    part_one,
    Broadcast,
    Pulse,
    Flipflop,
    Conjunction,
    Button,
    Network,
    to_tokens,
    PulseCounter,
)

AN_ID = "db"
ANOTHER_ID = "xd"


def test_to_tokens_should_convert_tokens():
    tokens = to_tokens(
        ["broadcaster -> a, b, c", "%a -> b", "%b -> c", "%c -> inv", "&inv -> a"]
    )

    assert list(tokens) == [
        ("broadcaster", "a"),
        ("broadcaster", "b"),
        ("broadcaster", "c"),
        ("%a", "b"),
        ("%b", "c"),
        ("%c", "inv"),
        ("&inv", "a"),
    ]


class TestNetwork:
    def test_it_should_set_modules_on_instantiation(self):
        network = Network(
            (
                ("broadcaster", "a"),
                ("broadcaster", "b"),
                ("broadcaster", "c"),
                ("%a", "b"),
                ("%b", "c"),
                ("%c", "inv"),
                ("&inv", "a"),
            )
        )

        assert set(network.modules.keys()) == {"broadcaster", "a", "b", "c", "inv"}
        assert isinstance(network.modules["broadcaster"], Broadcast)
        assert isinstance(network.modules["a"], Flipflop)
        assert isinstance(network.modules["b"], Flipflop)
        assert isinstance(network.modules["c"], Flipflop)
        assert isinstance(network.modules["inv"], Conjunction)

    def test_it_should_populate_inputs(self):
        network = Network(
            (
                ("broadcaster", "a"),
                ("broadcaster", "b"),
                ("broadcaster", "c"),
                ("%a", "b"),
                ("%b", "c"),
                ("%c", "inv"),
                ("&inv", "a"),
            )
        )

        assert network.modules["inv"].inputs == {"c": Pulse.LOW}

    def test_it_should_trigger(self):
        pass


class TestGivenButtonModule:
    def test_it_should_send_low_pulse(self):
        button = Button(AN_ID, PulseCounter())
        result = button.send()

        assert button.counter.low == 1
        assert result == {"id": AN_ID, "pulse": Pulse.LOW}


class TestGivenBroadcastModule:
    def test_it_should_send_low_pulse(self):
        broadcast = Broadcast(AN_ID, PulseCounter())
        result = broadcast.send()

        assert broadcast.counter.low == 1
        assert result == {"id": AN_ID, "pulse": Pulse.LOW}


class TestGivenFlipflopModule:
    def test_it_should_flip_when_receiving_low_pulse(self):
        flipflop = Flipflop(AN_ID, PulseCounter())
        flipflop.receive({"id": AN_ID, "pulse": Pulse.LOW})

        assert flipflop.on is True

    def test_it_should_flip_when_receiving_low_pulse_twice(self):
        flipflop = Flipflop(AN_ID, PulseCounter())

        flipflop.receive({"id": AN_ID, "pulse": Pulse.LOW})
        flipflop.receive({"id": AN_ID, "pulse": Pulse.LOW})

        assert flipflop.on is False

    def test_it_should_send_a_high_pulse_when_on(self):
        flipflop = Flipflop(AN_ID, PulseCounter())
        flipflop.on = True

        assert flipflop.send() == {"id": AN_ID, "pulse": Pulse.HIGH}

    def test_it_should_send_a_high_pulse_when_off(self):
        flipflop = Flipflop(AN_ID, PulseCounter())
        flipflop.on = False

        assert flipflop.send() == {"id": AN_ID, "pulse": Pulse.LOW}


class TestGivenConjunctionModule:
    def test_it_should_update_input_pulse_when_receiving_it(self):
        conjunction = Conjunction(AN_ID, PulseCounter())
        a_pulse = Pulse.HIGH

        conjunction.receive({"id": AN_ID, "pulse": a_pulse})

        assert conjunction.inputs[AN_ID] == a_pulse

    def test_it_should_send_a_low_pulse_when_all_inputs_last_pulse_is_high(self):
        conjunction = Conjunction(AN_ID, PulseCounter())
        conjunction.inputs[AN_ID] = Pulse.HIGH

        assert conjunction.send() == {"id": AN_ID, "pulse": Pulse.LOW}

    def test_it_should_send_a_high_pulse_when_any_input_is_low(self):
        conjunction = Conjunction(AN_ID, PulseCounter())
        conjunction.inputs[AN_ID] = Pulse.HIGH
        conjunction.inputs[ANOTHER_ID] = Pulse.LOW

        assert conjunction.send() == {"id": AN_ID, "pulse": Pulse.HIGH}

    def test_it_should_send_a_high_pulse_when_off(self):
        flipflop = Flipflop(AN_ID, PulseCounter())
        flipflop.on = False

        assert flipflop.send() == {"id": AN_ID, "pulse": Pulse.LOW}


def test_first_example():
    result = part_one(
        ["broadcaster -> a, b, c", "%a -> b", "%b -> c", "%c -> inv", "&inv -> a"]
    )

    assert result == 32000000
