from typing import Any, List, Optional, Tuple, Union

from ..lua import LuaNum
from ..sess import eval_lua


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


def open(side: str) -> None:
    return eval_lua(b'G:rednet:M:open', side).take_none()


def close(side: str = None) -> None:
    return eval_lua(b'G:rednet:M:close', side).take_none()


def send(receiverID: int, message: Any, protocol: str = None) -> bool:
    return eval_lua(b'G:rednet:M:send', receiverID, message, protocol).take_bool()


def broadcast(message: Any, protocol: str = None) -> None:
    return eval_lua(b'G:rednet:M:broadcast', message, protocol).take_none()


def receive(
    protocolFilter: str = None, timeout: LuaNum = None,
) -> Optional[Tuple[int, Any, Optional[str]]]:
    rp = eval_lua(b'G:rednet:M:receive', protocolFilter, timeout)
    if rp.peek() is None:
        return None
    return (rp.take_int(), rp.take(), rp.take_option_string())


def isOpen(side: str = None) -> bool:
    return eval_lua(b'G:rednet:M:isOpen', side).take_bool()


def host(protocol: str, hostname: str) -> None:
    return eval_lua(b'G:rednet:M:host', protocol, hostname).take_none()


def unhost(protocol: str) -> None:
    return eval_lua(b'G:rednet:M:unhost', protocol).take_none()


def lookup(protocol: str, hostname: str = None) -> Union[Optional[int], List[int]]:
    rp = eval_lua(b'G:rednet:M:lookup', protocol, hostname)
    if hostname is None:
        r = []
        while rp.peek() is not None:
            r.append(rp.take_int())
        return r
    else:
        return rp.take_option_int()
