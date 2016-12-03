from .base import BaseSubAPI, str_return


class KeysAPI(BaseSubAPI):
    _API = 'keys'

    async def getName(self, code: int) -> str:
        return str_return(await self._send('getName', code))
