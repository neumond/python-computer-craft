from typing import Tuple

from .base import BaseSubAPI, bool_return, int_return


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

    async def combine(self, *colors: int) -> int:
        return int_return(await self._send('combine', *colors))

    async def subtract(self, color_set: int, *colors: int) -> int:
        return int_return(await self._send('subtract', color_set, *colors))

    async def test(self, colors: int, color: int) -> bool:
        return bool_return(await self._send('test', colors, color))

    async def packRGB(self, r: float, g: float, b: float) -> int:
        return int_return(await self._send('packRGB', r, g, b))

    async def unpackRGB(self, rgb: int) -> Tuple[float, float, float]:
        ret = await self._send('unpackRGB', rgb)
        assert isinstance(ret, list)
        assert len(ret) == 3
        return tuple(ret)

    async def rgb8(self, *args):
        r = await self._send('rgb8', *args)
        return r[0] if len(r) == 1 else r
