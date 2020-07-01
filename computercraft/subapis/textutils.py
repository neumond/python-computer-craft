from typing import List, Union

from .base import BaseSubAPI, LuaNum
from ..rproc import nil, string, integer


class TextutilsAPI(BaseSubAPI):
    _API = 'textutils'

    async def slowWrite(self, text: str, rate: LuaNum = None):
        return nil(await self._send('slowWrite', text, rate))

    async def slowPrint(self, text: str, rate: LuaNum = None):
        return nil(await self._send('slowPrint', text, rate))

    async def formatTime(self, time: LuaNum, twentyFourHour: bool = None) -> str:
        return string(await self._send('formatTime', time, twentyFourHour))

    async def tabulate(self, *rows_and_colors: Union[list, int]):
        return nil(await self._send('tabulate', *rows_and_colors))

    async def pagedTabulate(self, *rows_and_colors: Union[list, int]):
        return nil(await self._send('pagedTabulate', *rows_and_colors))

    async def pagedPrint(self, text: str, freeLines: int = None) -> int:
        return integer(await self._send('pagedPrint', text, freeLines))

    def complete(self, partial: str, possible: List[str]) -> List[str]:
        return [p[len(partial):] for p in possible if p.startswith(partial)]

    # Questionable to implement
    # serialize
    # unserialize

    # Will not implement, use pythonic equivalents
    # serializeJSON
    # unserializeJSON
    # urlEncode
    # json_null
    # empty_json_array
