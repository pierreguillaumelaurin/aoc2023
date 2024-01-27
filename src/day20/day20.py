from abc import ABC, abstractmethod
from enum import Enum
from math import lcm
from typing import Dict, Iterable, List, Optional, Tuple, TypedDict

from pydot import Dot, Edge, Node

from src.utils import flatten


def parse_input():
    with open("input.dat", "r") as data:
        return [line.strip() for line in data.readlines()]


def visualize_input(input_: List[str]):
    def to_node_id(left: str) -> str:
        return left if left == "broadcaster" else left[1:]

    tokens = to_tokens(input_)
    nodes = set(token for token in tokens)
    graph = Dot("day20", graph_type="digraph", bgcolor="pink")

    for node in nodes:
        graph.add_node(Node(to_node_id(node[0]), label=node[0]))
    graph.add_node(Node("rx", label="Sandmover"))

    for token in tokens:
        graph.add_edge(Edge(to_node_id(token[0]), token[1]))

    graph.write("day20.dot")


def to_tokens(parsed_input: List[str]) -> List[Tuple[str, str]]:
    def lex(raw_communication: str) -> Multicast:
        tokens = [token.strip(",") for token in raw_communication.split(" ")]
        return {"sender": tokens[0], "receivers": tokens[2:]}

    def to_unicast(multicast: Multicast) -> List[Tuple[str, str]]:
        return [(multicast["sender"], receiver) for receiver in multicast["receivers"]]

    return flatten(to_unicast(lex(line)) for line in parsed_input)


def to_module_id(source_token: str):
    return (
        source_token
        if source_token == "broadcaster" or source_token == "button"
        else source_token[1:]
    )


def to_module_type(source_token: str):
    return (
        source_token
        if source_token == "broadcaster" or source_token == "button"
        else source_token[0]
    )


class Pulse(Enum):
    HIGH = "high"
    LOW = "low"


class Message(TypedDict):
    id: str
    pulse: Pulse


class PulseCounter:
    def __init__(self):
        self.high = 0
        self.low = 0


class Module(ABC):
    id: str

    def __init__(self, identifier: str, counter: PulseCounter):
        self.id = identifier
        self.counter = counter
        self.outputs = []

    @abstractmethod
    def send(self) -> Optional[Message]:
        pass

    @abstractmethod
    def receive(self, message: Message):
        pass

    def send_messages(self):
        messages = [self.send() for _ in self.outputs]

        for output, message in zip(self.outputs, messages):
            output.receive(message)

    def count_pulse(self, pulse: Pulse):
        match pulse:
            case Pulse.HIGH:
                self.counter.high += 1
            case Pulse.LOW:
                self.counter.low += 1


class Button(Module):
    def __init__(self, identifier: str, counter: PulseCounter):
        super().__init__(identifier, counter)

    def receive(self, message: Message):
        self.send_messages()

    def send(self):
        self.count_pulse(Pulse.LOW)
        return {"id": self.id, "pulse": Pulse.LOW}


class Broadcast(Module):
    def receive(self, message: Message):
        self.send_messages()

    def send(self):
        self.count_pulse(Pulse.LOW)
        return {"id": self.id, "pulse": Pulse.LOW}


class Flipflop(Module):
    def __init__(self, identifier: str, counter: PulseCounter):
        super().__init__(identifier, counter)
        self.on = False

    def receive(self, message: Message):
        if message["pulse"] == Pulse.LOW:
            self.on = not self.on
            self.send_messages()

    def send(self):
        pulse = Pulse.HIGH if self.on else Pulse.LOW

        self.count_pulse(pulse)
        return {"id": self.id, "pulse": pulse}


class Conjunction(Module):
    inputs: Dict[str, Pulse]

    def __init__(self, identifier: str, counter: PulseCounter):
        super().__init__(identifier, counter)
        self.inputs = {}
        self.cycle = False

    def receive(self, message: Message):
        self.inputs[message["id"]] = message["pulse"]
        self.send_messages()

    def send(self):
        pulses_on_high = (pulse == Pulse.HIGH for pulse in self.inputs.values())
        pulse = Pulse.LOW if all(pulses_on_high) else Pulse.HIGH

        if pulse == Pulse.HIGH:
            self.cycle = True

        self.count_pulse(pulse)
        return {"id": self.id, "pulse": pulse}


class SandMover(Module):
    def __init__(self, identifier: str, counter: PulseCounter):
        super().__init__(identifier, counter)
        self.on = False

    def receive(self, message: Message):
        if message["pulse"] == Pulse.LOW:
            self.on = True

    def send(self):
        pass


class Network:
    def __init__(self, tokens: Iterable[Tuple[str, str]]):
        self.modules = {}
        self.counter = PulseCounter()

        self._instantiate_modules(tokens)
        self._populate_conjunction_modules_inputs(tokens)
        self._populate_outputs(tokens)

    def _instantiate_modules(self, tokens: Iterable[Tuple[str, str]]):
        for token in tokens:
            module_id, module_type = to_module_id(token[0]), to_module_type(token[0])

            match module_type:
                case "%":
                    self.modules[module_id] = Flipflop(
                        identifier=module_id, counter=self.counter
                    )
                case "&":
                    self.modules[module_id] = Conjunction(
                        identifier=module_id, counter=self.counter
                    )
                case "broadcaster":
                    self.modules["broadcaster"] = Broadcast(
                        identifier=module_id, counter=self.counter
                    )
                case "button":
                    self.modules["button"] = Button(
                        identifier=module_id, counter=self.counter
                    )

        self._instantiate_module_with_no_outputs(tokens)

    def _instantiate_module_with_no_outputs(self, tokens):
        modules_with_no_output = set(token[1] for token in tokens) - set(
            self.modules.keys()
        )
        for module_id_with_no_output in modules_with_no_output:
            self.modules[module_id_with_no_output] = SandMover(
                identifier=module_id_with_no_output, counter=self.counter
            )

    def _populate_conjunction_modules_inputs(self, tokens: Iterable[Tuple[str, str]]):
        for token in tokens:
            source_module_id = to_module_id(token[0])
            destination_module_id = token[1]

            if isinstance(self.modules[destination_module_id], Conjunction):
                self.modules[destination_module_id].inputs[source_module_id] = Pulse.LOW

    def _populate_outputs(self, tokens: Iterable[Tuple[str, str]]):
        for token in tokens:
            source_module_id = to_module_id(token[0])
            destination_module_id = token[1]

            self.modules[source_module_id].outputs.append(
                self.modules[destination_module_id]
            )

    def trigger(self):
        self.counter.low += 1

        self.modules["broadcaster"].receive({"id": "button", "pulse": Pulse.LOW})


class Multicast(TypedDict):
    sender: str
    receivers: List[str]


class Pulses(TypedDict):
    high: int
    low: int


def part_one(raw_communications: List[str]) -> int:
    tokens = to_tokens(raw_communications)
    network = Network(tokens)

    for _ in range(1000):
        network.trigger()

    return network.counter.high * network.counter.low


def part_two(raw_communications: List[str]) -> int:
    def to_power_of_two(exponents: Iterable[int]):
        return (2**exponent for exponent in exponents)

    first_cycle_nodes_index_that_must_be_on = [0, 1, 2, 8, 9, 10, 11]
    second_cycle_nodes_index_that_must_be_on = [0, 1, 3, 4, 5, 6, 7, 8, 9, 10, 11]
    third_cycle_nodes_index_that_must_be_on = [0, 1, 4, 6, 8, 9, 10, 11]
    fourth_cycle_nodes_index_that_must_be_on = [0, 5, 7, 8, 9, 10, 11]

    return lcm(
        sum(to_power_of_two(first_cycle_nodes_index_that_must_be_on)),
        sum(to_power_of_two(second_cycle_nodes_index_that_must_be_on)),
        sum(to_power_of_two(third_cycle_nodes_index_that_must_be_on)),
        sum(to_power_of_two(fourth_cycle_nodes_index_that_must_be_on)),
    )


if __name__ == "__main__":
    # visualize_input(parse_input())
    print(part_one(parse_input()), part_two(parse_input()))
