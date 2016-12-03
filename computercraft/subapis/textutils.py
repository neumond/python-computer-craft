from typing import List, Union
from .base import BaseSubAPI, LuaNum, str_return, nil_return, int_return, list_return


class TextutilsAPI(BaseSubAPI):
    _API = 'textutils'

    async def slowWrite(self, text: str, rate: LuaNum):
        return nil_return(await self._send('slowWrite', text, rate))

    async def slowPrint(self, text: str, rate: LuaNum):
        return nil_return(await self._send('slowPrint', text, rate))

    async def formatTime(self, time: LuaNum, twentyFourHour: bool) -> str:
        return str_return(await self._send('formatTime', time, twentyFourHour))

    async def tabulate(self, *rows_and_colors: Union[list, int]):
        return nil_return(await self._send('tabulate', *rows_and_colors))

    async def pagedTabulate(self, *rows_and_colors: Union[list, int]):
        return nil_return(await self._send('pagedTabulate', *rows_and_colors))

    async def pagedPrint(self, text: str, freeLines: int=None) -> int:
        return int_return(await self._send('pagedPrint', text, freeLines))

    async def complete(self, partialName: str, environment: dict=None) -> List[str]:
        return list_return(await self._send('complete', partialName, environment))

    # Questionable to implement
    # serialize
    # unserialize

    # Will not implement, use pythonic equivalents
    # serializeJSON
    # urlEncode
