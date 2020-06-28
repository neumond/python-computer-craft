from ..errors import CommandException, ApiException
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


def bool_success(v):
    if v == [True]:
        return
    if len(v) == 2 and v[0] is False:
        assert isinstance(v[1], str)
        raise CommandException(v[1])
    raise ApiException('Bad return value: {}'.format(v))


def single_return(v):
    assert len(v) == 1
    return v[0]


def make_optional(fn):
    def op_fn(v):
        if v == []:
            return None
        return fn(v)
    return op_fn


def make_single_value_return(validator, converter=None):
    def fn(v):
        assert len(v) == 1
        if converter is not None:
            v[0] = converter(v[0])
        assert validator(v[0])
        return v[0]
    return fn


bool_return = make_single_value_return(lambda v: isinstance(v, bool))
int_return = make_single_value_return(lambda v: isinstance(v, int) and not isinstance(v, bool))
number_return = make_single_value_return(lambda v: isinstance(v, (int, float)) and not isinstance(v, bool))
str_return = make_single_value_return(lambda v: isinstance(v, str))
str_bool_return = make_single_value_return(lambda v: isinstance(v, (str, bool)))
list_return = make_single_value_return(
    lambda v: isinstance(v, list),
    lambda v: [] if v == {} else v,
)
dict_return = make_single_value_return(lambda v: isinstance(v, dict))


@make_optional
def nil_return(v):
    assert False


opt_bool_return = make_optional(bool_return)
opt_int_return = make_optional(int_return)
opt_number_return = make_optional(number_return)
opt_str_return = make_optional(str_return)
opt_str_bool_return = make_optional(str_bool_return)
opt_list_return = make_optional(list_return)
opt_dict_return = make_optional(dict_return)


class BaseSubAPI:
    _API = NotImplemented

    def __init__(self, cc):
        self._cc = cc

    async def _send(self, method, *params, omit_nulls=True):
        return await self._cc._send_cmd('return {}.{}({})'.format(
            self._API, method, lua_args(*params, omit_nulls=omit_nulls)
        ))
