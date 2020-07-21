from typing import List

from .. import ser
from ..sess import eval_lua_method_factory


method = eval_lua_method_factory('redstone.')


__all__ = (
    'getSides',
    'getInput',
    'setOutput',
    'getOutput',
    'getAnalogInput',
    'setAnalogOutput',
    'getAnalogOutput',
    'getBundledInput',
    'setBundledOutput',
    'getBundledOutput',
    'testBundledInput',
)


def getSides() -> List[str]:
    return method('getSides').take_list_of_strings()


def getInput(side: str) -> bool:
    return method('getInput', ser.encode(side)).take_bool()


def setOutput(side: str, value: bool):
    return method('setOutput', ser.encode(side), value).take_none()


def getOutput(side: str) -> bool:
    return method('getOutput', ser.encode(side)).take_bool()


def getAnalogInput(side: str) -> int:
    return method('getAnalogInput', ser.encode(side)).take_int()


def setAnalogOutput(side: str, strength: int):
    return method('setAnalogOutput', ser.encode(side), strength).take_none()


def getAnalogOutput(side: str) -> int:
    return method('getAnalogOutput', ser.encode(side)).take_int()


# bundled cables are not available in vanilla

def getBundledInput(side: str) -> int:
    return method('getBundledInput', ser.encode(side)).take_int()


def setBundledOutput(side: str, colors: int):
    return method('setBundledOutput', ser.encode(side), colors).take_none()


def getBundledOutput(side: str) -> int:
    return method('getBundledOutput', ser.encode(side)).take_int()


def testBundledInput(side: str, color: int) -> bool:
    return method('testBundledInput', ser.encode(side), color).take_bool()
