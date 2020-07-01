from typing import Tuple, List, Optional

from .base import BaseSubAPI
from ..rproc import tuple3_integer, any_dict, any_list, array_string, fact_tuple, boolean, option_integer


command_result = fact_tuple(boolean, array_string, option_integer, tail_nils=1)


class CommandsAPI(BaseSubAPI):
    async def exec(self, command: str) -> Tuple[bool, List[str], Optional[int]]:
        return command_result(await self._send('exec', command))

    async def list(self) -> List[str]:
        return array_string(await self._send('list'))

    async def getBlockPosition(self) -> Tuple[int, int, int]:
        return tuple3_integer(await self._send('getBlockPosition'))

    async def getBlockInfo(self, x: int, y: int, z: int) -> dict:
        return any_dict(await self._send('getBlockInfo', x, y, z))

    async def getBlockInfos(self, x1: int, y1: int, z1: int, x2: int, y2: int, z2: int) -> List[dict]:
        return any_list(await self._send('getBlockInfos', x1, y1, z1, x2, y2, z2))
