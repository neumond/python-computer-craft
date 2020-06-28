from typing import Tuple

from .base import BaseSubAPI
from ..rproc import boolean, integer, tuple3_number


class ColorsAPI(BaseSubAPI):
    _API = 'colors'

    white = 0x1
    orange = 0x2
    magenta = 0x4
    lightBlue = 0x8
    yellow = 0x10
    lime = 0x20
    pink = 0x40
    gray = 0x80
    lightGray = 0x100
    cyan = 0x200
    purple = 0x400
    blue = 0x800
    brown = 0x1000
    green = 0x2000
    red = 0x4000
    black = 0x8000

    # use these chars for term.blit
    chars = {
        '0': white,
        '1': orange,
        '2': magenta,
        '3': lightBlue,
        '4': yellow,
        '5': lime,
        '6': pink,
        '7': gray,
        '8': lightGray,
        '9': cyan,
        'a': purple,
        'b': blue,
        'c': brown,
        'd': green,
        'e': red,
        'f': black,
    }

    def __iter__(self):
        for c in self.chars.values():
            yield c

    # combine, subtract and test are mostly for redstone.setBundledOutput

    async def combine(self, *colors: int) -> int:
        return integer(await self._send('combine', *colors))

    async def subtract(self, color_set: int, *colors: int) -> int:
        return integer(await self._send('subtract', color_set, *colors))

    async def test(self, colors: int, color: int) -> bool:
        return boolean(await self._send('test', colors, color))

    async def packRGB(self, r: float, g: float, b: float) -> int:
        return integer(await self._send('packRGB', r, g, b))

    async def unpackRGB(self, rgb: int) -> Tuple[float, float, float]:
        return tuple3_number(await self._send('unpackRGB', rgb))
