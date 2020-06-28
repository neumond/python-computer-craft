from ..errors import ApiException
from typing import Union


LuaTable = Union[list, dict]
LuaNum = Union[int, float]


def lua_string(v):
    return '"{}"'.format(
        v.replace('\\', '\\\\')
        .replace('\a', '\\a')
        .replace('\b', '\\b')
        .replace('\f', '\\f')
        .replace('\n', '\\n')
        .replace('\r', '\\r')
        .replace('\t', '\\t')
        .replace('\v', '\\v')
        .replace('"', '\\"')
        .replace("'", "\\'")
        .replace('[', '\\[')
        .replace(']', '\\]')
    )


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
    raise ValueError('Can\'t convert a value to lua {}'.format(v))


def lua_args(*params, omit_nulls=True):
    ps, can_add = [], True
    for p in params:
        if omit_nulls and p is None:
            can_add = False
            continue
        if not can_add:
            raise ApiException('Optional parameter order error')
        ps.append(lua_value(p))
    return ', '.join(ps)


class BaseSubAPI:
    _API = NotImplemented

    def __init__(self, cc):
        self._cc = cc

    async def _send(self, method, *params, omit_nulls=True):
        return await self._cc._send_cmd('return {}.{}({})'.format(
            self._API, method, lua_args(*params, omit_nulls=omit_nulls)
        ))
