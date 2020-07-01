from typing import Optional

from .base import BaseSubAPI
from ..rproc import integer, nil, boolean, option_string


class MultishellAPI(BaseSubAPI):
    async def getCurrent(self) -> int:
        return integer(await self._send('getCurrent'))

    async def getCount(self) -> int:
        return integer(await self._send('getCount'))

    async def launch(self, environment: dict, programPath: str, *args: str) -> int:
        return integer(await self._send('launch', environment, programPath, *args))

    async def setTitle(self, tabID: int, title: str):
        return nil(await self._send('setTitle', tabID, title))

    async def getTitle(self, tabID: int) -> Optional[str]:
        return option_string(await self._send('getTitle', tabID))

    async def setFocus(self, tabID: int) -> bool:
        return boolean(await self._send('setFocus', tabID))

    async def getFocus(self) -> int:
        return integer(await self._send('getFocus'))
