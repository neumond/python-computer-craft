from typing import Optional, Union, List
from .base import (
    BaseSubAPI, lua_string,
    nil_return, opt_str_return, str_return, bool_return, int_return, list_return, opt_int_return,
)
from uuid import uuid4


class CCFile(BaseSubAPI):
    def __init__(self, cc, path, mode):
        super().__init__(cc)
        self._path = path
        self._mode = mode

    async def __aenter__(self):
        self._id = str(uuid4())
        self._API = 'temp[{}]'.format(lua_string(self._id))
        await self._cc._send_cmd('{} = fs.open({}, {})'.format(self._API, *map(lua_string, [
            self._path, self._mode
        ])))
        return self

    async def __aexit__(self, exc_type, exc, tb):
        await self._cc._send_cmd('{}.close(); {} = nil'.format(self._API, self._API))

    async def read(self) -> Optional[int]:
        return opt_int_return(await self._send('read'))

    async def readLine(self) -> Optional[str]:
        return opt_str_return(await self._send('readLine'))

    async def readAll(self) -> str:
        return str_return(await self._send('readAll'))

    async def write(self, data: Union[str, int]):
        return nil_return(await self._send('write', data))

    async def writeLine(self, data: str):
        return nil_return(await self._send('writeLine', data))

    async def flush(self):
        return nil_return(await self._send('flush'))

    def __aiter__(self):
        return self

    async def __anext__(self):
        line = await self.readLine()
        if line is None:
            raise StopAsyncIteration
        return line


class FSAPI(BaseSubAPI):
    _API = 'fs'

    async def list(self, path: str) -> List[str]:
        return list_return(await self._send('list', path))

    async def exists(self, path: str) -> bool:
        return bool_return(await self._send('exists', path))

    async def isDir(self, path: str) -> bool:
        return bool_return(await self._send('isDir', path))

    async def isReadOnly(self, path: str) -> bool:
        return bool_return(await self._send('isReadOnly', path))

    async def getName(self, path: str) -> str:
        return str_return(await self._send('getName', path))

    async def getDrive(self, path: str) -> Optional[str]:
        return opt_str_return(await self._send('getDrive', path))

    async def getSize(self, path: str) -> int:
        return int_return(await self._send('getSize', path))

    async def getFreeSpace(self, path: str) -> int:
        return int_return(await self._send('getFreeSpace', path))

    async def makeDir(self, path: str):
        return nil_return(await self._send('makeDir', path))

    async def move(self, fromPath: str, toPath: str):
        return nil_return(await self._send('move', fromPath, toPath))

    async def copy(self, fromPath: str, toPath: str):
        return nil_return(await self._send('copy', fromPath, toPath))

    async def delete(self, path: str):
        return nil_return(await self._send('delete', path))

    async def combine(self, basePath: str, localPath: str) -> str:
        return str_return(await self._send('combine', basePath, localPath))

    def open(self, path: str, mode: str) -> CCFile:
        '''
        Usage:

        async with api.fs.open('filename', 'w') as f:
            await f.writeLine('textline')

        async with api.fs.open('filename', 'r') as f:
            async for line in f:
                ...
        '''
        return CCFile(self._cc, path, mode)

    async def find(self, wildcard: str) -> List[str]:
        return list_return(await self._send('find', wildcard))

    async def getDir(self, path: str) -> str:
        return str_return(await self._send('getDir', path))

    async def complete(
        self, partialName: str, path: str, includeFiles: bool = None, includeSlashes: bool = None,
    ) -> List[str]:
        return list_return(await self._send('complete', partialName, path, includeFiles, includeSlashes))
