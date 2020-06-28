from typing import List, Dict

from .base import BaseSubAPI
from ..rproc import nil, string, boolean, integer, array_string, fact_mono_dict


map_string_string = fact_mono_dict(string, string)


class ShellAPI(BaseSubAPI):
    _API = 'shell'

    async def exit(self):
        return nil(await self._send('exit'))

    async def dir(self) -> str:
        return string(await self._send('dir'))

    async def setDir(self, path: str):
        return nil(await self._send('setDir', path))

    async def path(self) -> str:
        return string(await self._send('path'))

    async def setPath(self, path: str):
        return nil(await self._send('setPath', path))

    async def resolve(self, localPath: str) -> str:
        return string(await self._send('resolve', localPath))

    async def resolveProgram(self, name: str) -> str:
        return string(await self._send('resolveProgram', name))

    async def aliases(self) -> Dict[str, str]:
        return map_string_string(await self._send('aliases'))

    async def setAlias(self, alias: str, program: str):
        return nil(await self._send('setAlias', alias, program))

    async def clearAlias(self, alias: str):
        return nil(await self._send('clearAlias', alias))

    async def programs(self, showHidden: bool = None) -> List[str]:
        return array_string(await self._send('programs', showHidden))

    async def getRunningProgram(self) -> str:
        return string(await self._send('getRunningProgram'))

    async def run(self, command: str, *args: List[str]):
        return boolean(await self._send('run', command, *args))

    async def openTab(self, command: str, *args: List[str]) -> int:
        return integer(await self._send('openTab', command, *args))

    async def switchTab(self, tabID: int):
        return nil(await self._send('switchTab', tabID))

    async def complete(self, prefix: str) -> List[str]:
        return array_string(await self._send('complete', prefix))

    async def completeProgram(self, prefix: str) -> List[str]:
        return array_string(await self._send('completeProgram', prefix))

    # TODO: autocomplete functions
    # async def setCompletionFunction(self, path: str)
    # async def getCompletionInfo(self) -> LuaTable
