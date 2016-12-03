from typing import Tuple, Optional
from .base import BaseSubAPI, LuaNum


class GpsAPI(BaseSubAPI):
    _API = 'gps'

    async def locate(self, timeout: LuaNum=None, debug: bool=None) -> Optional[Tuple[int, int, int]]:
        r = await self._send('locate', timeout, debug)
        if r == [None]:
            return None
        return tuple(r)
