from typing import Any, List

from .base import BaseSubAPI
from ..rproc import nil, boolean, array_string


class SettingsAPI(BaseSubAPI):
    _API = 'settings'

    async def set(self, name: str, value: Any):
        return nil(await self._send('set', name, value))

    async def get(self, name: str, value=None) -> Any:
        return await self._send('get', name, value)

    async def unset(self, name: str):
        return nil(await self._send('unset', name))

    async def clear(self):
        return nil(await self._send('clear'))

    async def getNames(self) -> List[str]:
        return array_string(await self._send('getNames'))

    async def load(self, path: str) -> bool:
        return boolean(await self._send('load', path))

    async def save(self, path: str) -> bool:
        return boolean(await self._send('save', path))
