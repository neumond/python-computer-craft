from contextlib import asynccontextmanager
from typing import Optional, List

from .base import BaseSubAPI
from ..lua import lua_string
from ..rproc import boolean, string, integer, nil, array_string, option_string, fact_scheme_dict


attribute = fact_scheme_dict({
    'created': integer,
    'modification': integer,
    'isDir': boolean,
    'size': integer,
}, {})


class ReadHandle(BaseSubAPI):
    async def read(self, count: int) -> Optional[str]:
        return option_string(await self._send('read', count))

    async def readLine(self) -> Optional[str]:
        return option_string(await self._send('readLine'))

    async def readAll(self) -> str:
        return string(await self._send('readAll'))

    def __aiter__(self):
        return self

    async def __anext__(self):
        line = await self.readLine()
        if line is None:
            raise StopAsyncIteration
        return line


class WriteHandle(BaseSubAPI):
    async def write(self, text: str):
        return nil(await self._send('write', text))

    async def writeLine(self, text: str):
        return nil(await self._send('writeLine', text))

    async def flush(self):
        return nil(await self._send('flush'))


class FSAPI(BaseSubAPI):
    async def list(self, path: str) -> List[str]:
        return array_string(await self._send('list', path))

    async def exists(self, path: str) -> bool:
        return boolean(await self._send('exists', path))

    async def isDir(self, path: str) -> bool:
        return boolean(await self._send('isDir', path))

    async def isReadOnly(self, path: str) -> bool:
        return boolean(await self._send('isReadOnly', path))

    async def getDrive(self, path: str) -> Optional[str]:
        return option_string(await self._send('getDrive', path))

    async def getSize(self, path: str) -> int:
        return integer(await self._send('getSize', path))

    async def getFreeSpace(self, path: str) -> int:
        return integer(await self._send('getFreeSpace', path))

    async def getCapacity(self, path: str) -> int:
        return integer(await self._send('getCapacity', path))

    async def makeDir(self, path: str):
        return nil(await self._send('makeDir', path))

    async def move(self, fromPath: str, toPath: str):
        return nil(await self._send('move', fromPath, toPath))

    async def copy(self, fromPath: str, toPath: str):
        return nil(await self._send('copy', fromPath, toPath))

    async def delete(self, path: str):
        return nil(await self._send('delete', path))

    async def combine(self, basePath: str, localPath: str) -> str:
        return string(await self._send('combine', basePath, localPath))

    @asynccontextmanager
    async def open(self, path: str, mode: str):
        '''
        Usage:

        async with api.fs.open('filename', 'w') as f:
            await f.writeLine('textline')

        async with api.fs.open('filename', 'r') as f:
            async for line in f:
                ...
        '''
        fid = self._cc._new_task_id()
        var = 'temp[{}]'.format(lua_string(fid))
        await self._cc.eval_coro('{} = fs.open({}, {})'.format(
            var, lua_string(path), lua_string(mode)))
        try:
            yield (ReadHandle if 'r' in mode else WriteHandle)(self._cc, var)
        finally:
            await self._cc.eval_coro('{}.close(); {} = nil'.format(var, var))

    async def find(self, wildcard: str) -> List[str]:
        return array_string(await self._send('find', wildcard))

    async def getDir(self, path: str) -> str:
        return string(await self._send('getDir', path))

    async def getName(self, path: str) -> str:
        return string(await self._send('getName', path))

    async def isDriveRoot(self, path: str) -> bool:
        return boolean(await self._send('isDriveRoot', path))

    async def complete(
        self, partialName: str, path: str, includeFiles: bool = None, includeDirs: bool = None,
    ) -> List[str]:
        return array_string(await self._send(
            'complete', partialName, path, includeFiles, includeDirs))

    async def attributes(self, path: str) -> dict:
        return attribute(await self._send('attributes', path))
