from typing import Optional

from .base import BaseSubAPI, lua_string
from ..rproc import option_integer, option_string


class KeysAPI(BaseSubAPI):
    _API = 'keys'

    async def getCode(self, name: str) -> Optional[int]:
        # replaces properties
        # keys.space → await api.keys.getCode('space')
        return option_integer(await self._cc._send_cmd('''
if type({api}[{key}]) == 'number' then
    return {api}[{key}]
end
return nil'''.format(api=self._API, key=lua_string(name))))

    async def getName(self, code: int) -> Optional[str]:
        return option_string(await self._send('getName', code))
