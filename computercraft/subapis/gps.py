from typing import Tuple, Optional

from .base import BaseSubAPI
from ..lua import LuaNum
from ..rproc import tuple3_number, fact_option


option_tuple3_number = fact_option(tuple3_number)


class GpsAPI(BaseSubAPI):
    CHANNEL_GPS = 65534

    async def locate(self, timeout: LuaNum = None, debug: bool = None) -> Optional[Tuple[LuaNum, LuaNum, LuaNum]]:
        return option_tuple3_number(await self._send('locate', timeout, debug))
