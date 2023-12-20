from enum import Enum
from typing import TypedDict, Dict, List


def _parse():
    with open("input.dat", "r") as data:
        return [line.strip() for line in data.readlines()]


class Pulse(Enum):
    HIGH = 'high'
    LOW = 'low'


class ModuleType(Enum):
    BUTTON = 'button'
    BROADCAST = 'broadcast'
    FLIPFLOP = 'flipflop'
    CONJUNCTION = 'conjunction'

class Module(TypedDict):
    id: str
    type: ModuleType


class Communication(TypedDict):
    sender: Module
    receivers: List[str]


class CommunicationWithPulse(Communication):
    pulse: Pulse

class Broadcast(Module):
    pass


class Flipflop(Module):
    on: bool


class Conjunction(Module):
    connected_inputs: Dict[str, bool]

# sum of receivers in each communication


def part_one(raw_communications: List[str]) -> List[Pulse]:
    def tokenize(raw_communication: str):
        tokens = raw_communication.split(" ")
        return {
           'sender': tokens[0],
           'receivers': tokens[2:]
        }

    def to_module(raw_module: str) -> Module:
        if raw_module == "broadcaster":
            return {
                'id': "broadcaster",
                'type': ModuleType.BROADCAST
            }
        elif raw_module[0] == "%":
            return {
                'id': raw_module[1:],
                'type': ModuleType.FLIPFLOP,
                'on': False
            }
        else:
            return {
                'id': raw_module[1:],
                'type': ModuleType.CONJUNCTION,
                'on': False
            }


    def to_communication(token) -> Communication:
        return {
           'sender': to_module(token["sender"]),
            'receivers': [to_module(receiver) for receiver in token["receivers"]]
        }


    return [{'sender': {'id': 'button', 'type': 'button'}, 'pulse': Pulse.LOW, 'receivers': ["broadcaster"]}] + [tokenize(raw_communication) for raw_communication in raw_communications]

