from typing import Optional

from .base import BaseSubAPI
from ..lua import lua_string
from ..rproc import option_integer, option_string


class KeysAPI(BaseSubAPI):
    async def getCode(self, name: str) -> Optional[int]:
        # replaces properties
        # keys.space → await api.keys.getCode('space')
        return option_integer(await self._cc.eval_coro('''
if type({module}[{key}]) == 'number' then
    return {module}[{key}]
end
return nil'''.format(module=self.get_expr_code(), key=lua_string(name))))

    async def getName(self, code: int) -> Optional[str]:
        return option_string(await self._send('getName', code))
