from contextlib import contextmanager
from typing import Any, Dict, Optional, List

from ..sess import eval_lua, lua_context_object, ContextObject


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


class SeekMixin:
    def seek(self, whence: str = None, offset: int = None) -> int:
        # whence: set, cur, end
        rp = self._call(b'.seek', whence, offset)
        rp.check_nil_error()
        return rp.take_int()


class ReadMixin:
    def _take(self, rp):
        raise NotImplementedError

    def read(self, count: int = 1) -> Optional[str]:
        return self._take(self._call(b'.read', count))

    def readLine(self, withTrailing: bool = False) -> Optional[str]:
        return self._take(self._call(b'.readLine', withTrailing))

    def readAll(self) -> Optional[str]:
        return self._take(self._call(b'.readAll'))

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

    def write(self, text: str) -> None:
        return self._call(b'.write', self._put(text)).take_none()

    def flush(self) -> None:
        return self._call(b'.flush').take_none()


class ReadHandle(ReadMixin, ContextObject):
    def _take(self, rp):
        return rp.take_option_unicode()


class BinaryReadHandle(ReadMixin, SeekMixin, ContextObject):
    def _take(self, rp):
        return rp.take_option_bytes()


class WriteHandle(WriteMixin, ContextObject):
    def _put(self, t: str) -> bytes:
        return t.encode('utf-8')

    def writeLine(self, text: str) -> None:
        return self.write(text + '\n')


class BinaryWriteHandle(WriteMixin, SeekMixin, ContextObject):
    def _put(self, b: bytes) -> bytes:
        return b


def list(path: str) -> List[str]:
    return eval_lua(b'G:fs:M:list', path).take_list_of_strings()


def exists(path: str) -> bool:
    return eval_lua(b'G:fs:M:exists', path).take_bool()


def isDir(path: str) -> bool:
    return eval_lua(b'G:fs:M:isDir', path).take_bool()


def isReadOnly(path: str) -> bool:
    return eval_lua(b'G:fs:M:isReadOnly', path).take_bool()


def getDrive(path: str) -> Optional[str]:
    return eval_lua(b'G:fs:M:getDrive', path).take_option_string()


def getSize(path: str) -> int:
    return eval_lua(b'G:fs:M:getSize', path).take_int()


def getFreeSpace(path: str) -> int:
    return eval_lua(b'G:fs:M:getFreeSpace', path).take_int()


def getCapacity(path: str) -> int:
    return eval_lua(b'G:fs:M:getCapacity', path).take_int()


def makeDir(path: str) -> None:
    return eval_lua(b'G:fs:M:makeDir', path).take_none()


def move(fromPath: str, toPath: str) -> None:
    return eval_lua(b'G:fs:M:move', fromPath, toPath).take_none()


def copy(fromPath: str, toPath: str) -> None:
    return eval_lua(b'G:fs:M:copy', fromPath, toPath).take_none()


def delete(path: str) -> None:
    return eval_lua(b'G:fs:M:delete', path).take_none()


def combine(basePath: str, localPath: str) -> str:
    return eval_lua(b'G:fs:M:combine', basePath, localPath).take_string()


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
        b'fs.open(...)',
        (path, mode.replace('b', '') + 'b'),
        b'{e}.close()',
    ) as fid:
        if 'b' in mode:
            hcls = BinaryReadHandle if 'r' in mode else BinaryWriteHandle
        else:
            hcls = ReadHandle if 'r' in mode else WriteHandle
        yield hcls(fid)


def find(wildcard: str) -> List[str]:
    return eval_lua(b'G:fs:M:find', wildcard).take_list_of_strings()


def getDir(path: str) -> str:
    return eval_lua(b'G:fs:M:getDir', path).take_string()


def getName(path: str) -> str:
    return eval_lua(b'G:fs:M:getName', path).take_string()


def isDriveRoot(path: str) -> bool:
    return eval_lua(b'G:fs:M:isDriveRoot', path).take_bool()


def complete(
    partialName: str, path: str, includeFiles: bool = None, includeDirs: bool = None,
) -> List[str]:
    return eval_lua(
        b'G:fs:M:complete', partialName, path, includeFiles, includeDirs,
    ).take_list_of_strings()


def attributes(path: str) -> Dict[str, Any]:
    return eval_lua(b'G:fs:M:attributes', path).take_dict()
