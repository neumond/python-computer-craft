from typing import Any, List, Optional, Tuple, Union

from .. import ser
from ..lua import LuaNum
from ..sess import eval_lua_method_factory


method = eval_lua_method_factory('rednet.')


__all__ = (
    'CHANNEL_REPEAT',
    'CHANNEL_BROADCAST',
    'open',
    'close',
    'send',
    'broadcast',
    'receive',
    'isOpen',
    'host',
    'unhost',
    'lookup',
)


CHANNEL_REPEAT = 65533
CHANNEL_BROADCAST = 65535


def open(side: str):
    return method('open', ser.encode(side)).take_none()


def close(side: str = None):
    return method('close', ser.nil_encode(side)).take_none()


def send(receiverID: int, message: Any, protocol: str = None) -> bool:
    return method('send', receiverID, message, ser.nil_encode(protocol)).take_bool()


def broadcast(message: Any, protocol: str = None):
    return method('broadcast', message, ser.nil_encode(protocol)).take_none()


def receive(
    protocolFilter: str = None, timeout: LuaNum = None,
) -> Optional[Tuple[int, Any, Optional[str]]]:
    rp = method('receive', ser.nil_encode(protocolFilter), timeout)
    if rp.peek() is None:
        return None
    return (rp.take_int(), rp.take(), rp.take_option_string())


def isOpen(side: str = None) -> bool:
    return method('isOpen', ser.nil_encode(side)).take_bool()


def host(protocol: str, hostname: str):
    return method('host', ser.encode(protocol), ser.encode(hostname)).take_none()


def unhost(protocol: str):
    return method('unhost', ser.encode(protocol)).take_none()


def lookup(protocol: str, hostname: str = None) -> Union[Optional[int], List[int]]:
    rp = method('lookup', ser.encode(protocol), ser.nil_encode(hostname))
    if hostname is None:
        r = []
        while rp.peek() is not None:
            r.append(rp.take_int())
        return r
    else:
        return rp.take_option_int()
