from .base import BaseSubAPI
from ..lua import LuaTable


class WindowAPI(BaseSubAPI):
    _API = 'window'

    async def create(
        self, parentTerm: LuaTable, x: int, y: int, width: int, height: int, visible: bool = None,
    ) -> LuaTable:
        # TODO
        return await self._send('create', parentTerm, x, y, width, height, visible)
