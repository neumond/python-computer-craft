from typing import List

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
    return method('getInput', side).take_bool()


def setOutput(side: str, value: bool):
    return method('setOutput', side, value).take_none()


def getOutput(side: str) -> bool:
    return method('getOutput', side).take_bool()


def getAnalogInput(side: str) -> int:
    return method('getAnalogInput', side).take_int()


def setAnalogOutput(side: str, strength: int):
    return method('setAnalogOutput', side, strength).take_none()


def getAnalogOutput(side: str) -> int:
    return method('getAnalogOutput', side).take_int()


# bundled cables are not available in vanilla

def getBundledInput(side: str) -> int:
    return method('getBundledInput', side).take_int()


def setBundledOutput(side: str, colors: int):
    return method('setBundledOutput', side, colors).take_none()


def getBundledOutput(side: str) -> int:
    return method('getBundledOutput', side).take_int()


def testBundledInput(side: str, color: int) -> bool:
    return method('testBundledInput', side, color).take_bool()
