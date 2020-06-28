from typing import Any, List

from .base import BaseSubAPI, LuaNum
from ..rproc import nil, integer, boolean, array_integer


class RednetAPI(BaseSubAPI):
    _API = 'rednet'

    async def open(self, side: str):
        return nil(await self._send('open', side))

    async def close(self, side: str):
        return nil(await self._send('close', side))

    async def send(self, receiverID: int, message: Any, protocol: str = None):
        return nil(await self._send('send', receiverID, message, protocol))

    async def broadcast(self, message: Any, protocol: str = None):
        return nil(await self._send('broadcast', message, protocol))

    async def receive(self, protocolFilter: str = None, timeout: LuaNum = None) -> int:
        return integer(await self._send('receive', protocolFilter, timeout))

    async def isOpen(self, side: str) -> bool:
        return boolean(await self._send('isOpen', side))

    async def host(self, protocol: str, hostname: str):
        return nil(await self._send('host', protocol, hostname))

    async def unhost(self, protocol: str, hostname: str):
        return nil(await self._send('unhost', protocol, hostname))

    async def lookup(self, protocol: str, hostname: str) -> List[int]:
        return array_integer(await self._send('lookup', protocol, hostname))
