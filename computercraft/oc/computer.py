from typing import Optional, Union

# from .. import ser
from ..sess import eval_lua


__all__ = (
    'address',
    'tmpAddress',
    'freeMemory',
    'totalMemory',
    'energy',
    'maxEnergy',
    'uptime',
    'shutdown',
    'getBootAddress',
    'setBootAddress',
    'runlevel',
)


def address() -> str:
    # TODO: return UUID
    return eval_lua(b'R:computer:M:address').take_unicode()


def tmpAddress() -> str:
    # TODO: return UUID
    return eval_lua(b'R:computer:M:tmpAddress').take_unicode()


def freeMemory() -> int:
    return eval_lua(b'R:computer:M:freeMemory').take_int()


def totalMemory() -> int:
    return eval_lua(b'R:computer:M:totalMemory').take_int()


def energy() -> float:
    return eval_lua(b'R:computer:M:energy').take_number()


def maxEnergy() -> float:
    return eval_lua(b'R:computer:M:maxEnergy').take_number()


def uptime() -> float:
    return eval_lua(b'R:computer:M:uptime').take_number()


def shutdown(reboot: bool = False) -> None:
    # TODO: this function never returns
    return eval_lua(b'R:computer:M:shutdown', reboot).take_none()


def getBootAddress() -> str:
    # TODO: return UUID
    return eval_lua(b'R:computer:M:getBootAddress').take_unicode()


def setBootAddress(address: Optional[str] = None) -> None:
    # TODO: accept UUID
    return eval_lua(b'R:computer:M:setBootAddress', address).take_none()


def runlevel() -> Union[str, int]:
    return eval_lua(b'R:computer:M:runlevel').take_int_or_unicode()


# TODO:
# computer.users(): string, ...
# computer.addUser(name: string): boolean or nil, string
# computer.removeUser(name: string): boolean
# computer.pushSignal(name: string[, ...])
# computer.pullSignal([timeout: number]): name, ...
# computer.beep([frequency:string or number[, duration: number])
# computer.getDeviceInfo(): table
