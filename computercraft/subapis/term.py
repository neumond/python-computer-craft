from typing import Tuple
from .base import BaseSubAPI, list_return, nil_return
from .mixins import TermMixin


class CCWindow(BaseSubAPI, TermMixin):
    # TODO
    def __init__(self, cc):
        super().__init__(cc)

    async def setVisible(self, visibility: bool):
        return nil_return(await self._send('setVisible', visibility))

    async def redraw(self):
        return nil_return(await self._send('redraw'))

    async def restoreCursor(self):
        return nil_return(await self._send('restoreCursor'))

    async def getPosition(self) -> Tuple[int, int]:
        return tuple(await self._send('getPosition'))

    async def reposition(self, x: int, y: int, width: int=None, height: int=None):
        return nil_return(await self._send('reposition', x, y, width, height))


class TermAPI(BaseSubAPI, TermMixin):
    _API = 'term'

    # TODO
    # async def redirect

    # term.redirect(target) 	table previous terminal object
    # term.current() 	table terminal object
    # term.native() 	table terminal object
