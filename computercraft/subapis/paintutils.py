from typing import List

from .base import BaseSubAPI
from ..rproc import nil, integer, fact_array


array_2d_integer = fact_array(fact_array(integer))


class PaintutilsAPI(BaseSubAPI):
    async def parseImage(self, data: str) -> List[List[int]]:
        return array_2d_integer(await self._send('parseImage', data))

    async def loadImage(self, path: str) -> List[List[int]]:
        return array_2d_integer(await self._send('loadImage', path))

    async def drawPixel(self, x: int, y: int, color: int = None):
        return nil(await self._send('drawPixel', x, y, color))

    async def drawLine(self, startX: int, startY: int, endX: int, endY: int, color: int = None):
        return nil(await self._send('drawLine', startX, startY, endX, endY, color))

    async def drawBox(self, startX: int, startY: int, endX: int, endY: int, color: int = None):
        return nil(await self._send('drawBox', startX, startY, endX, endY, color))

    async def drawFilledBox(self, startX: int, startY: int, endX: int, endY: int, color: int = None):
        return nil(await self._send('drawFilledBox', startX, startY, endX, endY, color))

    async def drawImage(self, image: List[List[int]], xPos: int, yPos: int):
        return nil(await self._send('drawImage', image, xPos, yPos))
