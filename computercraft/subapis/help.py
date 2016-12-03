from typing import Optional, List
from .base import BaseSubAPI, nil_return, opt_str_return, str_return, list_return


class HelpAPI(BaseSubAPI):
    _API = 'help'

    async def path(self) -> str:
        return str_return(await self._send('path'))

    async def setPath(self, path: str):
        return nil_return(await self._send('setPath', path))

    async def lookup(self, topic: str) -> Optional[str]:
        return opt_str_return(await self._send('lookup', topic))

    async def topics(self) -> List[str]:
        return list_return(await self._send('topics'))

    async def completeTopic(self, topicPrefix: str) -> List[str]:
        return list_return(await self._send('completeTopic', topicPrefix))
