from contextlib import contextmanager
from typing import Optional, List, Union

from .base import BaseSubAPI
from ..errors import LuaException
from ..lua import lua_call
from ..rproc import boolean, string, integer, nil, array_string, option_string, option_integer, fact_scheme_dict
from ..sess import eval_lua_method_factory, lua_context_object


attribute = fact_scheme_dict({
    'created': integer,
    'modification': integer,
    'isDir': boolean,
    'size': integer,
}, {})


class SeekMixin:
    def seek(self, whence: str = None, offset: int = None) -> int:
        # whence: set, cur, end
        r = self._method('seek', whence, offset)
        if isinstance(r, list):
            assert r[0] is False
            raise LuaException(r[1])
        return integer(r)


class ReadHandle(BaseSubAPI):
    # TODO: binary handle must return bytes instead string

    def read(self, count: int = None) -> Optional[Union[str, int]]:
        r = self._method('read', count)
        return option_integer(r) if count is None else option_string(r)

    def readLine(self) -> Optional[str]:
        return option_string(self._method('readLine'))

    def readAll(self) -> str:
        return string(self._method('readAll'))

    def __iter__(self):
        return self

    def __next__(self):
        line = self.readLine()
        if line is None:
            raise StopIteration
        return line


class BinaryReadHandle(ReadHandle, SeekMixin):
    pass


class WriteHandle(BaseSubAPI):
    def write(self, text: str):
        return nil(self._method('write', text))

    def writeLine(self, text: str):
        return nil(self._method('writeLine', text))

    def flush(self):
        return nil(self._method('flush'))


class BinaryWriteHandle(WriteHandle, SeekMixin):
    pass


method = eval_lua_method_factory('fs.')


__all__ = (
    'list',
    'exists',
    'isDir',
    'isReadOnly',
    'getDrive',
    'getSize',
    'getFreeSpace',
    'getCapacity',
    'makeDir',
    'move',
    'copy',
    'delete',
    'combine',
    'open',
    'find',
    'getDir',
    'getName',
    'isDriveRoot',
    'complete',
    'attributes',
)


def list(path: str) -> List[str]:
    return array_string(method('list', path))


def exists(path: str) -> bool:
    return boolean(method('exists', path))


def isDir(path: str) -> bool:
    return boolean(method('isDir', path))


def isReadOnly(path: str) -> bool:
    return boolean(method('isReadOnly', path))


def getDrive(path: str) -> Optional[str]:
    return option_string(method('getDrive', path))


def getSize(path: str) -> int:
    return integer(method('getSize', path))


def getFreeSpace(path: str) -> int:
    return integer(method('getFreeSpace', path))


def getCapacity(path: str) -> int:
    return integer(method('getCapacity', path))


def makeDir(path: str):
    return nil(method('makeDir', path))


def move(fromPath: str, toPath: str):
    return nil(method('move', fromPath, toPath))


def copy(fromPath: str, toPath: str):
    return nil(method('copy', fromPath, toPath))


def delete(path: str):
    return nil(method('delete', path))


def combine(basePath: str, localPath: str) -> str:
    return string(method('combine', basePath, localPath))


@contextmanager
def open(path: str, mode: str):
    '''
    Usage:

    with fs.open('filename', 'w') as f:
        f.writeLine('textline')

    with fs.open('filename', 'r') as f:
        for line in f:
            ...
    '''
    with lua_context_object(
        lua_call('fs.open', path, mode),
        '{e}.close()',
    ) as var:
        if 'b' in mode:
            hcls = BinaryReadHandle if 'r' in mode else BinaryWriteHandle
        else:
            hcls = ReadHandle if 'r' in mode else WriteHandle
        yield hcls(var)


def find(wildcard: str) -> List[str]:
    return array_string(method('find', wildcard))


def getDir(path: str) -> str:
    return string(method('getDir', path))


def getName(path: str) -> str:
    return string(method('getName', path))


def isDriveRoot(path: str) -> bool:
    return boolean(method('isDriveRoot', path))


def complete(
    partialName: str, path: str, includeFiles: bool = None, includeDirs: bool = None,
) -> List[str]:
    return array_string(method(
        'complete', partialName, path, includeFiles, includeDirs))


def attributes(path: str) -> dict:
    return attribute(method('attributes', path))
