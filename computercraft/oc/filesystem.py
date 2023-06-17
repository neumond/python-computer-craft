from contextlib import contextmanager
from typing import List, Optional, Tuple, Union
from uuid import UUID

from ..sess import eval_lua, lua_context_object, ContextObject


__all__ = (
    'isAutorunEnabled',
    'setAutorunEnabled',
    'canonical',
    'segments',
    'concat',
    'path',
    'name',
    'mount',
    'mounts',
    'umount',
    'isLink',
    'link',
    'get',
    'exists',
    'size',
    'isDirectory',
    'lastModified',
    'list',
    'makeDirectory',
    'remove',
    'rename',
    'copy',
    'File',
    'open',
)


def isAutorunEnabled() -> bool:
    return eval_lua(b'R:filesystem:M:isAutorunEnabled').take_bool()


def setAutorunEnabled(value: bool) -> None:
    return eval_lua(b'R:filesystem:M:setAutorunEnabled', value).take_none()


def canonical(path: str) -> str:
    return eval_lua(b'R:filesystem:M:canonical', path).take_string()


def segments(path: str) -> List[str]:
    return eval_lua(b'R:filesystem:M:segments', path).take_list_of_strings()


def concat(pathA: str, pathB: str, *paths: str) -> str:
    return eval_lua(b'R:filesystem:M:concat', pathA, pathB, *paths).take_string()


def path(path: str) -> str:
    return eval_lua(b'R:filesystem:M:path', path).take_string()


def name(path: str) -> str:
    return eval_lua(b'R:filesystem:M:name', path).take_string()


# TODO: implement:
# filesystem.proxy(filter: string): table or nil, string
# same as component.proxy


def mount(fs: UUID, path: str) -> bool:
    # TODO: support component object as parameter
    r = eval_lua(b'R:filesystem:M:mount', fs, path)
    r.check_nil_error()
    return r.take_bool()


def mounts() -> List[Tuple[UUID, str]]:
    r = eval_lua(
        b'R:filesystem:local r={};'
        b'for c,t in _m.filesystem.mounts() do '
        b'r[#r+1]=c.address;r[#r+1]=t;end;return r').take_proc()
    o = []
    while r.peek() is not None:
        addr = r.take_uuid()
        path = r.take_string()
        o.append((addr, path))
    return o


def umount(fsOrPath: Union[UUID, str]) -> bool:
    # TODO: support component object as parameter
    return eval_lua(b'R:filesystem:M:umount', fsOrPath).take_bool()


def isLink(path: str) -> Tuple[bool, Optional[str]]:
    r = eval_lua(b'R:filesystem:M:isLink', path)
    is_link = r.take_bool()
    target = r.take_option_string()
    return is_link, target


def link(target: str, linkpath: str) -> bool:
    r = eval_lua(b'R:filesystem:M:link', target, linkpath)
    r.check_nil_error()
    return r.take_bool()


def get(path: str) -> Tuple[UUID, str]:
    r = eval_lua(
        b'R:filesystem:local a,b=_m.filesystem.get(...);'
        b'if a then a=a.address end;return a,b', path)
    r.check_nil_error()
    addr = r.take_uuid()
    target = r.take_string()
    return addr, target


def exists(path: str) -> bool:
    return eval_lua(b'R:filesystem:M:exists', path).take_bool()


def size(path: str) -> int:
    return eval_lua(b'R:filesystem:M:size', path).take_int()


def isDirectory(path: str) -> bool:
    return eval_lua(b'R:filesystem:M:isDirectory', path).take_bool()


def lastModified(path: str) -> float:
    return eval_lua(b'R:filesystem:M:lastModified', path).take_number()


def list(path: str) -> List[str]:
    r = eval_lua(
        b'R:filesystem:local r={};'
        b'for n in _m.filesystem.list(...) do r[#r+1]=n end;return r',
        path)
    r.check_nil_error()
    return r.take_list_of_strings()


def makeDirectory(path: str) -> bool:
    r = eval_lua(b'R:filesystem:M:makeDirectory', path)
    r.check_nil_error()
    return r.take_bool()


def remove(path: str) -> bool:
    r = eval_lua(b'R:filesystem:M:remove', path)
    r.check_nil_error()
    return r.take_bool()


def rename(oldPath: str, newPath: str) -> bool:
    r = eval_lua(b'R:filesystem:M:rename', oldPath, newPath)
    r.check_nil_error()
    return r.take_bool()


def copy(fromPath: str, toPath: str) -> bool:
    r = eval_lua(b'R:filesystem:M:copy', fromPath, toPath)
    r.check_nil_error()
    return r.take_bool()


class File(ContextObject):
    def read(self, n: int) -> Optional[bytes]:
        r = self._call(b':read', n)
        r.check_nil_error(allow_nil_nil=True)
        return r.take_option_bytes()

    def seek(self, whence: str, offset: int = 0) -> int:
        r = self._call(b':seek', whence, offset)
        r.check_nil_error()
        return r.take_int()

    def write(self, data: bytes) -> bool:
        r = self._call(b':write', data)
        r.check_nil_error()
        return r.take_bool()


@contextmanager
def open(path: str, mode: str = 'r'):
    with lua_context_object(
        b'_m.filesystem.open(...)',
        (path, mode),
        b'{e}:close()',
        b'R:filesystem:',
    ) as fid:
        yield File(fid)
