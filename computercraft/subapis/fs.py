from contextlib import contextmanager
from typing import Optional, List

from .base import BaseSubAPI
from .. import ser
from ..sess import eval_lua_method_factory, lua_context_object


class SeekMixin:
    def seek(self, whence: str = None, offset: int = None) -> int:
        # whence: set, cur, end
        rp = self._method('seek', ser.nil_encode(whence), offset)
        rp.check_nil_error()
        return rp.take_int()


class ReadMixin:
    def _take(self, rp):
        raise NotImplementedError

    def read(self, count: int = 1) -> Optional[str]:
        return self._take(self._method('read', count))

    def readLine(self, withTrailing: bool = False) -> Optional[str]:
        return self._take(self._method('readLine', withTrailing))

    def readAll(self) -> Optional[str]:
        return self._take(self._method('readAll'))

    def __iter__(self):
        return self

    def __next__(self):
        line = self.readLine()
        if line is None:
            raise StopIteration
        return line


class WriteMixin:
    def _put(self, t):
        raise NotImplementedError

    def write(self, text: str):
        return self._method('write', self._put(text)).take_none()

    def flush(self):
        return self._method('flush').take_none()


class ReadHandle(ReadMixin, BaseSubAPI):
    def _take(self, rp):
        return rp.take_option_unicode()


class BinaryReadHandle(ReadMixin, SeekMixin, BaseSubAPI):
    def _take(self, rp):
        return rp.take_option_bytes()


class WriteHandle(WriteMixin, BaseSubAPI):
    def _put(self, t: str) -> bytes:
        return t.encode('utf-8')

    def writeLine(self, text: str):
        return self.write(text + '\n')


class BinaryWriteHandle(WriteMixin, SeekMixin, BaseSubAPI):
    def _put(self, b: bytes) -> bytes:
        return b


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
    return method('list', ser.encode(path)).take_list_of_strings()


def exists(path: str) -> bool:
    return method('exists', ser.encode(path)).take_bool()


def isDir(path: str) -> bool:
    return method('isDir', ser.encode(path)).take_bool()


def isReadOnly(path: str) -> bool:
    return method('isReadOnly', ser.encode(path)).take_bool()


def getDrive(path: str) -> Optional[str]:
    return method('getDrive', ser.encode(path)).take_option_string()


def getSize(path: str) -> int:
    return method('getSize', ser.encode(path)).take_int()


def getFreeSpace(path: str) -> int:
    return method('getFreeSpace', ser.encode(path)).take_int()


def getCapacity(path: str) -> int:
    return method('getCapacity', ser.encode(path)).take_int()


def makeDir(path: str):
    return method('makeDir', ser.encode(path)).take_none()


def move(fromPath: str, toPath: str):
    return method('move', ser.encode(fromPath), ser.encode(toPath)).take_none()


def copy(fromPath: str, toPath: str):
    return method('copy', ser.encode(fromPath), ser.encode(toPath)).take_none()


def delete(path: str):
    return method('delete', ser.encode(path)).take_none()


def combine(basePath: str, localPath: str) -> str:
    return method('combine', ser.encode(basePath), ser.encode(localPath)).take_string()


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
        'fs.open(...)',
        (ser.encode(path), ser.encode(mode.replace('b', '') + 'b')),
        '{e}.close()',
    ) as var:
        if 'b' in mode:
            hcls = BinaryReadHandle if 'r' in mode else BinaryWriteHandle
        else:
            hcls = ReadHandle if 'r' in mode else WriteHandle
        yield hcls(var)


def find(wildcard: str) -> List[str]:
    return method('find', ser.encode(wildcard)).take_list_of_strings()


def getDir(path: str) -> str:
    return method('getDir', ser.encode(path)).take_string()


def getName(path: str) -> str:
    return method('getName', ser.encode(path)).take_string()


def isDriveRoot(path: str) -> bool:
    return method('isDriveRoot', ser.encode(path)).take_bool()


def complete(
    partialName: str, path: str, includeFiles: bool = None, includeDirs: bool = None,
) -> List[str]:
    return method(
        'complete', ser.encode(partialName), ser.encode(path), includeFiles, includeDirs,
    ).take_list_of_strings()


def attributes(path: str) -> dict:
    tp = method('attributes', ser.encode(path)).take_dict((
        b'created',
        b'modification',
        b'isDir',
        b'size',
    ))
    r = {}
    r['created'] = tp.take_int()
    r['modification'] = tp.take_int()
    r['isDir'] = tp.take_bool()
    r['size'] = tp.take_int()
    return r
