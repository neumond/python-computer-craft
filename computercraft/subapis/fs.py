from contextlib import asynccontextmanager
from typing import Optional, List, Union

from .base import BaseSubAPI
from ..errors import LuaException
from ..lua import lua_args
from ..rproc import boolean, string, integer, nil, array_string, option_string, option_integer, fact_scheme_dict


attribute = fact_scheme_dict({
    'created': integer,
    'modification': integer,
    'isDir': boolean,
    'size': integer,
}, {})


class SeekMixin:
    async def seek(self, whence: str = None, offset: int = None) -> int:
        # whence: set, cur, end
        r = await self._send('seek', whence, offset)
        if isinstance(r, list):
            assert r[0] is False
            raise LuaException(r[1])
        return integer(r)


class ReadHandle(BaseSubAPI):
    async def read(self, count: int = None) -> Optional[Union[str, int]]:
        r = await self._send('read', count)
        return option_integer(r) if count is None else option_string(r)

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


class BinaryReadHandle(ReadHandle, SeekMixin):
    pass


class WriteHandle(BaseSubAPI):
    async def write(self, text: str):
        return nil(await self._send('write', text))

    async def writeLine(self, text: str):
        return nil(await self._send('writeLine', text))

    async def flush(self):
        return nil(await self._send('flush'))


class BinaryWriteHandle(WriteHandle, SeekMixin):
    pass


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
        create_expr = '{}.open({})'.format(
            self.get_expr_code(),
            lua_args(path, mode),
        )
        fin_tpl = '{e}.close()'
        async with self._cc._create_temp_object(create_expr, fin_tpl) as var:
            if 'b' in mode:
                hcls = BinaryReadHandle if 'r' in mode else BinaryWriteHandle
            else:
                hcls = ReadHandle if 'r' in mode else WriteHandle
            yield hcls(self._cc, var)

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
