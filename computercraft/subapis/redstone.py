from typing import List

from ..sess import eval_lua


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
    return eval_lua(b'G:redstone:M:getSides').take_list_of_strings()


def getInput(side: str) -> bool:
    return eval_lua(b'G:redstone:M:getInput', side).take_bool()


def setOutput(side: str, value: bool) -> None:
    return eval_lua(b'G:redstone:M:setOutput', side, value).take_none()


def getOutput(side: str) -> bool:
    return eval_lua(b'G:redstone:M:getOutput', side).take_bool()


def getAnalogInput(side: str) -> int:
    return eval_lua(b'G:redstone:M:getAnalogInput', side).take_int()


def setAnalogOutput(side: str, strength: int) -> None:
    return eval_lua(b'G:redstone:M:setAnalogOutput', side, strength).take_none()


def getAnalogOutput(side: str) -> int:
    return eval_lua(b'G:redstone:M:getAnalogOutput', side).take_int()


# bundled cables are not available in vanilla

def getBundledInput(side: str) -> int:
    return eval_lua(b'G:redstone:M:getBundledInput', side).take_int()


def setBundledOutput(side: str, colors: int):
    return eval_lua(b'G:redstone:M:setBundledOutput', side, colors).take_none()


def getBundledOutput(side: str) -> int:
    return eval_lua(b'G:redstone:M:getBundledOutput', side).take_int()


def testBundledInput(side: str, color: int) -> bool:
    return eval_lua(b'G:redstone:M:testBundledInput', side, color).take_bool()
