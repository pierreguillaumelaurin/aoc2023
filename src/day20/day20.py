from enum import Enum
from itertools import islice
from typing import TypedDict, Dict, List, Tuple

from src.utils import flatten


def parse_input():
    with open("input.dat", "r") as data:
        return [line.strip() for line in data.readlines()]


class Pulse(Enum):
    HIGH = "high"
    LOW = "low"


class ModuleType(Enum):
    BUTTON = "button"
    BROADCAST = "broadcast"
    FLIPFLOP = "flipflop"
    CONJUNCTION = "conjunction"


# TODO refactor module typing

class Module(TypedDict):
    type: ModuleType


class Multicast(TypedDict):
    sender: str
    receivers: List[str]


class MulticastWithPulse(Multicast):
    pulse: Pulse


class Broadcast(Module):
    pass


class Flipflop(Module):
    on: bool


class Conjunction(Module):
    connected_inputs: Dict[str, bool]


class Pulses(TypedDict):
    high: int
    low: int


class NetworkState(TypedDict):
    modules: Dict
    pulses: Pulses


# sum of receivers in each communication


def part_one(raw_communications: List[str]):
    # TODO refactor using less concepts
    def lex(raw_communication: str) -> Multicast:
        tokens = [token.strip(",") for token in raw_communication.split(" ")]
        return {"sender": tokens[0], "receivers": tokens[2:]}

    def to_communications(multicast: Multicast) -> List[Tuple[str, str]]:
        return [(multicast["sender"], receiver) for receiver in multicast["receivers"]]

    def to_communication_by_time(
            raw_communications: List[str],
    ) -> List[Tuple[str, str]]:
        communications_groups = (
            to_communications(lex(raw_communication))
            for raw_communication in raw_communications
        )

        return [("button", "broadcaster")] + flatten(communications_groups)

    # TODO type state
    def to_next_state(previous, communication) -> NetworkState:
        source_module_type = communication[0][0]
        destination_module_type = communication[1][0]

        # TODO separate into functions
        # send pulse
        # TODO refactor for ifs
        last_pulse: Pulse
        match source_module_type:
            case "%":
                if previous["modules"][communication[0][1:]]["latest_pulse"] == Pulse.LOW:
                    pass
                elif previous["modules"][communication[0][1:]]["on"] is False:
                    previous["pulses"]["high"] += 1
                    last_pulse = Pulse.HIGH
                    receive_pulse(previous, communication, last_pulse)
                else:
                    previous["pulses"]["low"] += 1
                    last_pulse = Pulse.LOW
                    receive_pulse(previous, communication, last_pulse)
            case '&':
                if all(pulse == Pulse.HIGH for pulse in previous["modules"][
                                                                      communication[0][1:]]["inputs"].values()):
                    previous["pulses"]["low"] += 1
                    last_pulse = Pulse.LOW
                    receive_pulse(previous, communication, last_pulse)
                else:
                    previous["pulses"]["high"] += 1
                    last_pulse = Pulse.HIGH
                    receive_pulse(previous, communication, last_pulse)
            case _:
                previous["pulses"]["low"] += 1
                last_pulse = Pulse.LOW
                receive_pulse(previous, communication, last_pulse)

        # receive pulse

        return previous

    def receive_pulse(previous, communication, last_pulse):
        destination_module_type = previous["modules"][communication[1]]["type"]

        if destination_module_type == ModuleType.FLIPFLOP and last_pulse == Pulse.LOW:
            previous[communication[1]]["on"] = not previous[communication[1]]["on"]
        elif destination_module_type == ModuleType.BROADCAST:
            previous[communication[1]]["inputs"][communication[0]] = last_pulse

    def get_initial_state(communications: List[Tuple[str, str]]) -> NetworkState:
        modules = {}
        # TODO set initial state outside of function

        for communication in communications:
            module_id = communication[0] if communication[0][0] == "b" else communication[0][1:]
            if communication[0][0] == '%':
                modules[module_id] = {"type": ModuleType.FLIPFLOP, "on": False, "latest_pulse": Pulse}
            elif communication[0][0] == '&':
                modules[module_id] = {"type": ModuleType.CONJUNCTION, "inputs": {}}
            elif communication[0] == 'broadcaster':
                modules['broadcaster'] = {"type": ModuleType.BROADCAST}
            elif communication[0] == 'button':
                modules['button'] = {"type": ModuleType.BUTTON}

        for communication in communications:
            if modules[communication[1]]["type"] == ModuleType.CONJUNCTION and communication[0][0] == "b":
                modules[communication[1]]["inputs"][communication[0]] = Pulse.LOW
            elif modules[communication[1]]["type"] == ModuleType.CONJUNCTION:
                modules[communication[1]]["inputs"][communication[0][1:]] = Pulse.LOW
        return {"modules": modules, "pulses": {"high": 0, "low": 0}}

    def network_state(communications: List[Tuple[str, str]], initial_state: NetworkState):
        state: NetworkState = initial_state

        for communication in communications:
            state = to_next_state(state, communication)
            yield state

    times_button_pressed = 1000
    communications = to_communication_by_time(raw_communications)

    network_states = network_state(
        times_button_pressed * to_communication_by_time(raw_communications), get_initial_state(communications)
    )

    # TODO extract?
    for _ in range(times_button_pressed - 1):
        next(network_states)
    final_state = next(network_states)
    return final_state["pulses"]["high"] * final_state["pulses"]["low"]

