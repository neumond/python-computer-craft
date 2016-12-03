from typing import Tuple
from .base import bool_return, nil_return, int_return


class TermMixin:
    async def write(self, text: str):
        return nil_return(await self._send('write', text))

    async def blit(self, text: str, textColors: str, backgroundColors: str):
        return nil_return(await self._send('blit', text, textColors, backgroundColors))

    async def clear(self):
        return nil_return(await self._send('clear'))

    async def clearLine(self):
        return nil_return(await self._send('clearLine'))

    async def getCursorPos(self) -> Tuple[int, int]:
        return tuple(await self._send('getCursorPos'))

    async def setCursorPos(self, x: int, y: int):
        return nil_return(await self._send('setCursorPos', x, y))

    async def setCursorBlink(self, value: bool):
        return nil_return(await self._send('setCursorBlink', value))

    async def isColor(self) -> bool:
        return bool_return(await self._send('isColor'))

    async def getSize(self) -> Tuple[int, int]:
        return tuple(await self._send('getSize'))

    async def scroll(self, n: int):
        return nil_return(await self._send('scroll', n))

    async def setTextColor(self, color: int):
        return nil_return(await self._send('setTextColor', color))

    async def getTextColor(self) -> int:
        return int_return(await self._send('getTextColor'))

    async def setBackgroundColor(self, color: int):
        return nil_return(await self._send('setBackgroundColor', color))

    async def getBackgroundColor(self) -> int:
        return int_return(await self._send('getBackgroundColor'))
