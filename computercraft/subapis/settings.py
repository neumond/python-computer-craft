from typing import Any, List

from ..sess import eval_lua


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
        options[b'description'] = description
    if default is not None:
        options[b'default'] = default
    if type is not None:
        options[b'type'] = type
    return eval_lua(b'G:settings:M:define', name, options).take_none()


def undefine(name: str) -> None:
    return eval_lua(b'G:settings:M:undefine', name).take_none()


def getDetails(name: str) -> dict:
    tp = eval_lua(b'G:settings:M:getDetails', name).take_dict((
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


def set(name: str, value: Any) -> None:
    return eval_lua(b'G:settings:M:set', name, value).take_none()


def get(name: str, default: Any = None) -> Any:
    return eval_lua(b'G:settings:M:get', name, default).take()


def unset(name: str) -> None:
    return eval_lua(b'G:settings:M:unset', name).take_none()


def clear() -> None:
    return eval_lua(b'G:settings:M:clear').take_none()


def getNames() -> List[str]:
    return eval_lua(b'G:settings:M:getNames').take_list_of_strings()


def load(path: str = None) -> bool:
    return eval_lua(b'G:settings:M:load', path).take_bool()


def save(path: str = None) -> bool:
    return eval_lua(b'G:settings:M:save', path).take_bool()
