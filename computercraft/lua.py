from typing import Union

from . import ser


LuaTable = Union[list, dict]
LuaNum = Union[int, float]


class LuaExpr:
    def get_expr_code(self):
        raise NotImplementedError


_tmap = {
    '\\': '\\\\',
    '\a': '\\a',
    '\b': '\\b',
    '\f': '\\f',
    '\n': '\\n',
    '\r': '\\r',
    '\t': '\\t',
    '\v': '\\v',
    '"': '\\"',
    "'": "\\'",
    '[': '\\[',
    ']': '\\]',
}
_tmap = {ord(c): r for c, r in _tmap.items()}


def lua_string(v):
    if isinstance(v, bytes):
        v = ser.decode(v)
    return '"{}"'.format(v.translate(_tmap))
