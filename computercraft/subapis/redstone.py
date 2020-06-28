from typing import List

from .base import BaseSubAPI
from ..rproc import boolean, nil, integer, array_string


class RedstoneAPI(BaseSubAPI):
    _API = 'redstone'

    async def getSides(self) -> List[str]:
        return array_string(await self._send('getSides'))

    async def getInput(self, side: str) -> bool:
        return boolean(await self._send('getInput', side))

    async def setOutput(self, side: str, value: bool):
        return nil(await self._send('setOutput', side, value))

    async def getOutput(self, side: str) -> bool:
        return boolean(await self._send('getOutput', side))

    async def getAnalogInput(self, side: str) -> int:
        return integer(await self._send('getAnalogInput', side))

    async def setAnalogOutput(self, side: str, strength: int):
        return nil(await self._send('setAnalogOutput', side, strength))

    async def getAnalogOutput(self, side: str) -> int:
        return integer(await self._send('getAnalogOutput', side))

    async def getBundledInput(self, side: str) -> int:
        return integer(await self._send('getBundledInput', side))

    async def setBundledOutput(self, side: str, colors: int):
        return nil(await self._send('setBundledOutput', side, colors))

    async def getBundledOutput(self, side: str) -> int:
        return integer(await self._send('getBundledOutput', side))

    async def testBundledInput(self, side: str, color: int) -> bool:
        return boolean(await self._send('testBundledInput', side, color))
