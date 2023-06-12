from typing import Optional, Union
from uuid import UUID

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


def address() -> UUID:
    return eval_lua(b'R:computer:M:address').take_uuid()


def tmpAddress() -> UUID:
    return eval_lua(b'R:computer:M:tmpAddress').take_uuid()


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


def getBootAddress() -> UUID:
    return eval_lua(b'R:computer:M:getBootAddress').take_uuid()


def setBootAddress(address: Optional[UUID] = None) -> None:
    return eval_lua(b'R:computer:M:setBootAddress', address).take_none()


def runlevel() -> Union[str, int]:
    r = eval_lua(b'R:computer:M:runlevel')
    if r.peek_type() is bytes:
        return r.take_string()
    return r.take_int()


# TODO:
# computer.users(): string, ...
# computer.addUser(name: string): boolean or nil, string
# computer.removeUser(name: string): boolean
# computer.pushSignal(name: string[, ...])
# computer.pullSignal([timeout: number]): name, ...
# computer.beep([frequency:string or number[, duration: number])
# computer.getDeviceInfo(): table
