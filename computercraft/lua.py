from typing import Union


LuaTable = Union[list, dict]
LuaNum = Union[int, float]


class LuaExpr:
    def get_expr_code(self):
        raise NotImplementedError


class ArbLuaExpr(LuaExpr):
    def __init__(self, code: str):
        self._code = code

    def get_expr_code(self):
        return self._code


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


def lua_list(v):
    return '{' + ', '.join(lua_value(x) for x in v) + '}'


def lua_dict(v):
    return '{' + ', '.join(
        '[{}]={}'.format(lua_value(k), lua_value(v)) for k, v in v.items()
    ) + '}'


def lua_value(v):
    if v is None:
        return 'nil'
    if v is False:
        return 'false'
    if v is True:
        return 'true'
    if isinstance(v, str):
        return lua_string(v)
    if isinstance(v, (int, float)):
        return str(v)
    if isinstance(v, list):
        return lua_list(v)
    if isinstance(v, dict):
        return lua_dict(v)
    if isinstance(v, LuaExpr):
        return v.get_expr_code()
    raise ValueError('Can\'t convert a value to lua {}'.format(v))


def lua_args(*params):
    for idx in range(len(params) - 1, -1, -1):
        if params[idx] is not None:
            break
    else:
        idx = -1
    params = params[:idx + 1]
    return ', '.join(lua_value(p) for p in params)


def lua_call(name, *params):
    return '{}({})'.format(name, lua_args(*params))


def return_lua_call(name, *params):
    return 'return ' + lua_call(name, *params)
