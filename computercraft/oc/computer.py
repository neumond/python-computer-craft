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
    return eval_lua(b'R:computer.address').take_unicode()


def tmpAddress() -> str:
    return eval_lua(b'R:computer.tmpAddress').take_unicode()


def freeMemory() -> int:
    return eval_lua(b'R:computer.freeMemory').take_int()


def totalMemory() -> int:
    return eval_lua(b'R:computer.totalMemory').take_int()


def energy() -> float:
    return eval_lua(b'R:computer.energy').take_number()


def maxEnergy() -> float:
    return eval_lua(b'R:computer.maxEnergy').take_number()


def uptime() -> float:
    return eval_lua(b'R:computer.uptime').take_number()


def shutdown(reboot: bool = False) -> None:
    # TODO: this function never returns
    return eval_lua(b'R:computer.shutdown', reboot).take_none()


def getBootAddress() -> str:
    return eval_lua(b'R:computer.getBootAddress').take_unicode()


def setBootAddress(address: Optional[str] = None) -> None:
    return eval_lua(b'R:computer.setBootAddress', address).take_none()


def runlevel() -> Union[str, int]:
    return eval_lua(b'R:computer.runlevel').take_int_or_unicode()


# TODO:
# computer.users(): string, ...
# computer.addUser(name: string): boolean or nil, string
# computer.removeUser(name: string): boolean
# computer.pushSignal(name: string[, ...])
# computer.pullSignal([timeout: number]): name, ...
# computer.beep([frequency:string or number[, duration: number])
# computer.getDeviceInfo(): table
