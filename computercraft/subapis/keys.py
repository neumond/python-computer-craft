from typing import Optional

from .base import BaseSubAPI, lua_string, opt_int_return, opt_str_return


class KeysAPI(BaseSubAPI):
    _API = 'keys'

    async def getCode(self, name: str) -> Optional[int]:
        # replaces properties
        # keys.space → await api.keys.getCode('space')
        return opt_int_return(await self._cc._send_cmd('''
if type({api}[{key}]) == 'number' then
    return {api}[{key}]
end
return nil'''.format(api=self._API, key=lua_string(name))))

    async def getName(self, code: int) -> Optional[str]:
        return opt_str_return(await self._send('getName', code))
