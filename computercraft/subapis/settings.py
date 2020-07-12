from typing import Any, List

from ..rproc import nil, boolean, string, array_string, fact_scheme_dict
from ..sess import eval_lua_method_factory


setting = fact_scheme_dict({
    'changed': boolean,
}, {
    'description': string,
    'default': lambda v: v,
    'type': string,
    'value': lambda v: v,
})
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
        options['description'] = description
    if default is not None:
        options['default'] = default
    if type is not None:
        options['type'] = type
    return nil(method('define', name, options))


def undefine(name: str):
    return nil(method('undefine', name))


def getDetails(name: str) -> dict:
    return setting(method('getDetails', name))


def set(name: str, value: Any):
    return nil(method('set', name, value))


def get(name: str, default: Any = None) -> Any:
    return method('get', name, default)


def unset(name: str):
    return nil(method('unset', name))


def clear():
    return nil(method('clear'))


def getNames() -> List[str]:
    return array_string(method('getNames'))


def load(path: str = None) -> bool:
    return boolean(method('load', path))


def save(path: str = None) -> bool:
    return boolean(method('save', path))
