from contextlib import asynccontextmanager
from typing import Tuple

from ..lua import lua_args
from ..rproc import nil, tuple2_integer, tuple3_string
from .base import BaseSubAPI
from .mixins import TermMixin, TermTarget


class CCWindow(BaseSubAPI, TermMixin):
    async def setVisible(self, visibility: bool):
        return nil(await self._send('setVisible', visibility))

    async def redraw(self):
        return nil(await self._send('redraw'))

    async def restoreCursor(self):
        return nil(await self._send('restoreCursor'))

    async def getPosition(self) -> Tuple[int, int]:
        return tuple2_integer(await self._send('getPosition'))

    async def reposition(self, x: int, y: int, width: int = None, height: int = None, parent: TermTarget = None):
        return nil(await self._send('reposition', x, y, width, height, parent))

    async def getLine(self, y: int) -> Tuple[str, str, str]:
        return tuple3_string(await self._send('getLine', y))

    def get_term_target(self) -> TermTarget:
        return TermTarget(self.get_expr_code())


class WindowAPI(BaseSubAPI):
    @asynccontextmanager
    async def create(
        self, parentTerm: TermTarget, x: int, y: int, width: int, height: int, visible: bool = None,
    ) -> CCWindow:
        create_expr = '{}.create({})'.format(
            self.get_expr_code(),
            lua_args(parentTerm, x, y, width, height, visible),
        )
        async with self._cc._create_temp_object(create_expr) as var:
            yield CCWindow(self._cc, var)
