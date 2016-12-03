from typing import List
from .base import BaseSubAPI, str_return, int_return, nil_return, bool_return


class MultishellAPI(BaseSubAPI):
    _API = 'multishell'

    async def getCurrent(self) -> int:
        return int_return(await self._send('getCurrent'))

    async def getCount(self) -> int:
        return int_return(await self._send('getCount'))

    async def launch(self, environment: dict, programPath: str, *args: List[str]) -> int:
        return int_return(await self._send('launch', environment, programPath, *args))

    async def setFocus(self, tabID: int):
        return bool_return(await self._send('setFocus', tabID))

    async def setTitle(self, tabID: int, title: str):
        return nil_return(await self._send('setTitle', tabID, title))

    async def getTitle(self, tabID: int) -> str:
        return str_return(await self._send('getTitle', tabID))

    async def getFocus(self) -> int:
        return int_return(await self._send('getFocus'))
