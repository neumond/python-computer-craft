from typing import Any, List
from .base import BaseSubAPI, list_return, nil_return, single_return, bool_return


class SettingsAPI(BaseSubAPI):
    _API = 'settings'

    async def set(self, name: str, value):
        return nil_return(await self._send('set', name, value))

    async def get(self, name: str, value=None) -> Any:
        return single_return(await self._send('get', name, value))

    async def unset(self, name: str):
        return nil_return(await self._send('unset', name))

    async def clear(self):
        return nil_return(await self._send('clear'))

    async def getNames(self) -> List[str]:
        return list_return(await self._send('getNames'))

    async def load(self, path: str) -> bool:
        return bool_return(await self._send('load', path))

    async def save(self, path: str) -> bool:
        return bool_return(await self._send('save', path))
