from typing import Any, List, Optional, Tuple, Union

from .base import BaseSubAPI
from ..lua import LuaNum
from ..rproc import nil, integer, option_string, boolean, array_integer, option_integer, fact_option, fact_tuple


recv_result = fact_option(fact_tuple(
    integer,
    lambda v: v,
    option_string,
    tail_nils=1,
))


class RednetAPI(BaseSubAPI):
    CHANNEL_REPEAT = 65533
    CHANNEL_BROADCAST = 65535

    async def open(self, side: str):
        return nil(await self._send('open', side))

    async def close(self, side: str = None):
        return nil(await self._send('close', side))

    async def send(self, receiverID: int, message: Any, protocol: str = None) -> bool:
        return boolean(await self._send('send', receiverID, message, protocol))

    async def broadcast(self, message: Any, protocol: str = None):
        return nil(await self._send('broadcast', message, protocol))

    async def receive(
        self, protocolFilter: str = None, timeout: LuaNum = None,
    ) -> Optional[Tuple[int, Any, Optional[str]]]:
        return recv_result(await self._send('receive', protocolFilter, timeout))

    async def isOpen(self, side: str = None) -> bool:
        return boolean(await self._send('isOpen', side))

    async def host(self, protocol: str, hostname: str):
        return nil(await self._send('host', protocol, hostname))

    async def unhost(self, protocol: str):
        return nil(await self._send('unhost', protocol))

    async def lookup(self, protocol: str, hostname: str = None) -> Union[Optional[int], List[int]]:
        result = await self._send('lookup', protocol, hostname)
        if hostname is None:
            if result is None:
                return []
            if isinstance(result, list):
                return array_integer(result)
            return [integer(result)]
        else:
            return option_integer(result)
