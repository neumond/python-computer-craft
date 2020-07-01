from typing import Optional, List

from .base import BaseSubAPI
from ..rproc import string, nil, array_string, option_string


class HelpAPI(BaseSubAPI):
    async def path(self) -> str:
        return string(await self._send('path'))

    async def setPath(self, path: str):
        return nil(await self._send('setPath', path))

    async def lookup(self, topic: str) -> Optional[str]:
        return option_string(await self._send('lookup', topic))

    async def topics(self) -> List[str]:
        return array_string(await self._send('topics'))

    async def completeTopic(self, topicPrefix: str) -> List[str]:
        return array_string(await self._send('completeTopic', topicPrefix))
