from .base import BaseSubAPI
from ..rproc import flat_try_result


class PocketAPI(BaseSubAPI):
    _API = 'pocket'

    async def equipBack(self):
        return flat_try_result(await self._send('equipBack'))

    async def unequipBack(self) -> bool:
        return flat_try_result(await self._send('unequipBack'))
