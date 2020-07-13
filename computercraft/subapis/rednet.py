from typing import Any, List, Optional, Tuple, Union

from ..lua import LuaNum
from ..rproc import nil, integer, option_string, boolean, array_integer, option_integer, fact_option, fact_tuple
from ..sess import eval_lua_method_factory


recv_result = fact_option(fact_tuple(
    integer,
    lambda v: v,
    option_string,
    tail_nils=1,
))
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
    return nil(method('open', side))


def close(side: str = None):
    return nil(method('close', side))


def send(receiverID: int, message: Any, protocol: str = None) -> bool:
    return boolean(method('send', receiverID, message, protocol))


def broadcast(message: Any, protocol: str = None):
    return nil(method('broadcast', message, protocol))


def receive(
    protocolFilter: str = None, timeout: LuaNum = None,
) -> Optional[Tuple[int, Any, Optional[str]]]:
    return recv_result(method('receive', protocolFilter, timeout))


def isOpen(side: str = None) -> bool:
    return boolean(method('isOpen', side))


def host(protocol: str, hostname: str):
    return nil(method('host', protocol, hostname))


def unhost(protocol: str):
    return nil(method('unhost', protocol))


def lookup(protocol: str, hostname: str = None) -> Union[Optional[int], List[int]]:
    result = method('lookup', protocol, hostname)
    if hostname is None:
        if result is None:
            return []
        if isinstance(result, list):
            return array_integer(result)
        return [integer(result)]
    else:
        return option_integer(result)
