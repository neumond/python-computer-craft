from typing import Tuple, List, Optional

from .base import BaseSubAPI
from ..errors import CommandException
from ..rproc import tuple3_integer, any_dict, any_list, array_string, integer


class CommandsAPI(BaseSubAPI):
    _API = 'commands'

    async def exec(self, command: str) -> Tuple[str, Optional[int]]:
        # TODO: use rproc
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
        return integer(await self._send('execAsync', command))

    async def list(self) -> List[str]:
        return array_string(await self._send('list'))

    async def getBlockPosition(self) -> Tuple[int, int, int]:
        return tuple3_integer(await self._send('getBlockPosition'))

    async def getBlockInfo(self, x: int, y: int, z: int) -> dict:
        return any_dict(await self._send('getBlockInfo', x, y, z))

    async def getBlockInfos(self, x1: int, y1: int, z1: int, x2: int, y2: int, z2: int) -> List[dict]:
        return any_list(await self._send('getBlockInfos', x1, y1, z1, x2, y2, z2))
