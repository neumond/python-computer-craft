from typing import Union


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
    return '"{}"'.format(v.translate(_tmap))
