from typing import Tuple

from .base import BaseSubAPI
from .mixins import TermMixin
from ..rproc import nil, tuple2_integer, tuple3_number


class CCWindow(BaseSubAPI, TermMixin):
    # TODO
    def __init__(self, cc):
        super().__init__(cc)

    async def setVisible(self, visibility: bool):
        return nil(await self._send('setVisible', visibility))

    async def redraw(self):
        return nil(await self._send('redraw'))

    async def restoreCursor(self):
        return nil(await self._send('restoreCursor'))

    async def getPosition(self) -> Tuple[int, int]:
        return tuple2_integer(await self._send('getPosition'))

    async def reposition(self, x: int, y: int, width: int = None, height: int = None):
        return nil(await self._send('reposition', x, y, width, height))


class TermAPI(BaseSubAPI, TermMixin):
    _API = 'term'

    async def nativePaletteColor(self, colorID: int) -> Tuple[float, float, float]:
        return tuple3_number(await self._send('nativePaletteColor', colorID))

    # TODO
    # term.redirect(target) 	table previous terminal object
    # term.current() 	table terminal object
    # term.native() 	table terminal object
