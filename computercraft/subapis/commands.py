from typing import Tuple, List
from .base import BaseSubAPI, int_return, list_return, dict_return


class CommandsAPI(BaseSubAPI):
    _API = 'commands'

    async def exec(self, command: str):
        r = await self._send('exec', command)
        assert len(r) == 2
        assert isinstance(r[0], bool)
        assert isinstance(r[1], list)
        return r[0], r[1]

    async def execAsync(self, command: str) -> int:
        return int_return(await self._send('execAsync', command))

    async def list(self) -> List[str]:
        return list_return(await self._send('list'))

    async def getBlockPosition(self) -> Tuple[int, int, int]:
        return tuple(await self._send('getBlockPosition'))

    async def getBlockInfo(self, x: int, y: int, z: int) -> dict:
        return dict_return(await self._send('getBlockInfo', x, y, z))

    async def getBlockInfos(self, x1: int, y1: int, z1: int, x2: int, y2: int, z2: int) -> List[dict]:
        return list_return(await self._send('getBlockInfos', x1, y1, z1, x2, y2, z2))
