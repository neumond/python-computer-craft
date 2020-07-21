from typing import Any, List

from .. import ser
from ..sess import eval_lua_method_factory


method = eval_lua_method_factory('settings.')


__all__ = (
    'define',
    'undefine',
    'getDetails',
    'set',
    'get',
    'unset',
    'clear',
    'getNames',
    'load',
    'save',
)


def define(name: str, description: str = None, default: Any = None, type: str = None):
    options = {}
    if description is not None:
        options[b'description'] = ser.encode(description)
    if default is not None:
        options[b'default'] = default
    if type is not None:
        options[b'type'] = ser.encode(type)
    return method('define', ser.encode(name), options).take_none()


def undefine(name: str):
    return method('undefine', ser.encode(name)).take_none()


def getDetails(name: str) -> dict:
    tp = method('getDetails', ser.encode(name)).take_dict((
        b'changed',
        b'description',
        b'default',
        b'type',
        b'value',
    ))
    r = {}
    r['changed'] = tp.take_bool()
    for k, v in [
        ('description', tp.take_option_string()),
        ('default', tp.take()),
        ('type', tp.take_option_string()),
        ('value', tp.take()),
    ]:
        if v is not None:
            r[k] = v
    return r


def set(name: str, value: Any):
    return method('set', ser.encode(name), value).take_none()


def get(name: str, default: Any = None) -> Any:
    return method('get', ser.encode(name), default).take()


def unset(name: str):
    return method('unset', ser.encode(name)).take_none()


def clear():
    return method('clear').take_none()


def getNames() -> List[str]:
    return method('getNames').take_list_of_strings()


def load(path: str = None) -> bool:
    return method('load', ser.nil_encode(path)).take_bool()


def save(path: str = None) -> bool:
    return method('save', ser.nil_encode(path)).take_bool()
