from typing import Any, List

from .base import BaseSubAPI
from ..rproc import nil, boolean, string, array_string, fact_scheme_dict


setting = fact_scheme_dict({
    'changed': boolean,
}, {
    'description': string,
    'default': lambda v: v,
    'type': string,
    'value': lambda v: v,
})


class SettingsAPI(BaseSubAPI):
    _API = 'settings'

    async def define(self, name: str, description: str = None, default: Any = None, type: str = None):
        options = {}
        if description is not None:
            options['description'] = description
        if default is not None:
            options['default'] = default
        if type is not None:
            options['type'] = type
        return nil(await self._send('define', name, options))

    async def undefine(self, name: str):
        return nil(await self._send('undefine', name))

    async def getDetails(self, name: str) -> dict:
        return setting(await self._send('getDetails', name))

    async def set(self, name: str, value: Any):
        return nil(await self._send('set', name, value))

    async def get(self, name: str, default: Any = None) -> Any:
        return await self._send('get', name, default)

    async def unset(self, name: str):
        return nil(await self._send('unset', name))

    async def clear(self):
        return nil(await self._send('clear'))

    async def getNames(self) -> List[str]:
        return array_string(await self._send('getNames'))

    async def load(self, path: str = None) -> bool:
        return boolean(await self._send('load', path))

    async def save(self, path: str = None) -> bool:
        return boolean(await self._send('save', path))
