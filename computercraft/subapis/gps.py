from typing import Tuple, Optional
from .base import BaseSubAPI, LuaNum


class GpsAPI(BaseSubAPI):
    _API = 'gps'

    CHANNEL_GPS = 65534

    async def locate(self, timeout: LuaNum = None, debug: bool = None) -> Optional[Tuple[int, int, int]]:
        r = await self._send('locate', timeout, debug, omit_nulls=False)
        if r == []:
            return None
        assert isinstance(r, list)
        assert len(r) == 3
        return tuple(r)
