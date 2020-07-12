from typing import Optional, List

from ..rproc import string, nil, array_string, option_string
from ..sess import eval_lua_method_factory


method = eval_lua_method_factory('help.')


__all__ = (
    'path',
    'setPath',
    'lookup',
    'topics',
    'completeTopic',
)


def path() -> str:
    return string(method('path'))


def setPath(path: str):
    return nil(method('setPath', path))


def lookup(topic: str) -> Optional[str]:
    return option_string(method('lookup', topic))


def topics() -> List[str]:
    return array_string(method('topics'))


def completeTopic(topicPrefix: str) -> List[str]:
    return array_string(method('completeTopic', topicPrefix))
