from typing import List, Dict
from .base import BaseSubAPI, nil_return, str_return, bool_return, int_return, dict_return, list_return


class ShellAPI(BaseSubAPI):
    _API = 'shell'

    async def exit(self):
        return nil_return(await self._send('exit'))

    async def dir(self) -> str:
        return str_return(await self._send('dir'))

    async def setDir(self, path: str):
        return nil_return(await self._send('setDir', path))

    async def path(self) -> str:
        return str_return(await self._send('path'))

    async def setPath(self, path: str):
        return nil_return(await self._send('setPath', path))

    async def resolve(self, localPath: str) -> str:
        return str_return(await self._send('resolve', localPath))

    async def resolveProgram(self, name: str) -> str:
        return str_return(await self._send('resolveProgram', name))

    async def aliases(self) -> Dict[str, str]:
        return dict_return(await self._send('aliases'))

    async def setAlias(self, alias: str, program: str):
        return nil_return(await self._send('setAlias', alias, program))

    async def clearAlias(self, alias: str):
        return nil_return(await self._send('clearAlias', alias))

    async def programs(self, showHidden: bool = None) -> List[str]:
        return list_return(await self._send('programs', showHidden))

    async def getRunningProgram(self) -> str:
        return str_return(await self._send('getRunningProgram'))

    async def run(self, command: str, *args: List[str]):
        return bool_return(await self._send('run', command, *args))

    async def openTab(self, command: str, *args: List[str]) -> int:
        return int_return(await self._send('openTab', command, *args))

    async def switchTab(self, tabID: int):
        return nil_return(await self._send('switchTab', tabID))

    async def complete(self, prefix: str) -> List[str]:
        return list_return(await self._send('complete', prefix))

    async def completeProgram(self, prefix: str) -> List[str]:
        return list_return(await self._send('completeProgram', prefix))

    # TODO: autocomplete functions
    # async def setCompletionFunction(self, path: str)
    # async def getCompletionInfo(self) -> LuaTable
