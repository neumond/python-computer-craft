from typing import Optional

from .base import BaseSubAPI, opt_str_return


class KeysAPI(BaseSubAPI):
    _API = 'keys'

    async def getName(self, code: int) -> Optional[str]:
        return opt_str_return(await self._send('getName', code))
