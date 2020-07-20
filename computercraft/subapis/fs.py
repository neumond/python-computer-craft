import builtins
from contextlib import contextmanager
from typing import Optional, List

from .base import BaseSubAPI
from ..errors import LuaException
from ..lua import lua_call, lua_args, lua_string
from ..rproc import boolean, string, integer, nil, array_string, option_string, fact_scheme_dict
from ..sess import eval_lua, eval_lua_method_factory, lua_context_object


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
        if isinstance(r, builtins.list):
            assert r[0] is False
            raise LuaException(r[1])
        return integer(r)


class ReadHandle(BaseSubAPI):
    def _decode(self, b):
        return b.decode('utf-8')

    def _read(self, name, params, val):
        code = '''
local s = {}.{}({})
if s == nil then return nil end
s = s:gsub('.', function(c) return string.format('%02X', string.byte(c)) end)
return s
'''.lstrip().format(
            self.get_expr_code(), name, lua_args(*params),
        )
        return self._decode(bytes.fromhex(val(eval_lua(code))))

    def read(self, count: int = 1) -> Optional[str]:
        return self._read('read', (count, ), option_string)

    def readLine(self) -> Optional[str]:
        return self._read('readLine', (), option_string)

    def readAll(self) -> str:
        return self._read('readAll', (), string)

    def __iter__(self):
        return self

    def __next__(self):
        line = self.readLine()
        if line is None:
            raise StopIteration
        return line


class BinaryReadHandle(ReadHandle, SeekMixin):
    def _decode(self, b):
        return b


class WriteHandle(BaseSubAPI):
    def _encode(self, s):
        return s.encode('utf-8')

    def _write(self, name, text, val):
        code = '''
local s = {}
s = s:gsub('..', function(cc) return string.char(tonumber(cc, 16)) end)
return {}.{}(s)
'''.lstrip().format(
            lua_string(self._encode(text).hex()),
            self.get_expr_code(), name,
        )
        return val(eval_lua(code))

    def write(self, text: str):
        return nil(self._method('write', text))

    def writeLine(self, text: str):
        return nil(self._method('writeLine', text))

    def flush(self):
        return nil(self._method('flush'))


class BinaryWriteHandle(WriteHandle, SeekMixin):
    def _encode(self, s):
        return s


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
        lua_call('fs.open', path, mode.replace('b', '') + 'b'),
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
