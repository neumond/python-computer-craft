from typing import Tuple, List, Optional
from .base import BaseSubAPI, int_return, list_return, dict_return
from ..errors import CommandException


class CommandsAPI(BaseSubAPI):
    _API = 'commands'

    async def exec(self, command: str) -> Tuple[str, Optional[int]]:
        r = await self._send('exec', command)
        assert len(r) == 3
        assert isinstance(r[0], bool)

        if r[1] == {}:
            r[1] = []
        assert isinstance(r[1], list)
        r[1] = '\n'.join(r[1])

        if r[2] is None:
            r[2] = 0
        assert isinstance(r[2], int)

        if r[0] is False:
            raise CommandException(r[1])

        return r[1], r[2]

    async def execAsync(self, command: str) -> int:
        return int_return(await self._send('execAsync', command))

    async def list(self) -> List[str]:
        return list_return(await self._send('list'))

    async def getBlockPosition(self) -> Tuple[int, int, int]:
        ret = await self._send('getBlockPosition')
        assert isinstance(ret, list)
        assert len(ret) == 3
        return tuple(ret)

    async def getBlockInfo(self, x: int, y: int, z: int) -> dict:
        return dict_return(await self._send('getBlockInfo', x, y, z))

    async def getBlockInfos(self, x1: int, y1: int, z1: int, x2: int, y2: int, z2: int) -> List[dict]:
        return list_return(await self._send('getBlockInfos', x1, y1, z1, x2, y2, z2))
