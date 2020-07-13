from typing import List

from ..rproc import boolean, nil, integer, array_string
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
    return array_string(method('getSides'))


def getInput(side: str) -> bool:
    return boolean(method('getInput', side))


def setOutput(side: str, value: bool):
    return nil(method('setOutput', side, value))


def getOutput(side: str) -> bool:
    return boolean(method('getOutput', side))


def getAnalogInput(side: str) -> int:
    return integer(method('getAnalogInput', side))


def setAnalogOutput(side: str, strength: int):
    return nil(method('setAnalogOutput', side, strength))


def getAnalogOutput(side: str) -> int:
    return integer(method('getAnalogOutput', side))


# bundled cables are not available in vanilla

def getBundledInput(side: str) -> int:
    return integer(method('getBundledInput', side))


def setBundledOutput(side: str, colors: int):
    return nil(method('setBundledOutput', side, colors))


def getBundledOutput(side: str) -> int:
    return integer(method('getBundledOutput', side))


def testBundledInput(side: str, color: int) -> bool:
    return boolean(method('testBundledInput', side, color))
