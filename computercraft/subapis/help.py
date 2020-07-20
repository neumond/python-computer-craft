from typing import Optional, List

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
    return method('path').take_string()


def setPath(path: str):
    return method('setPath', path).take_none()


def lookup(topic: str) -> Optional[str]:
    return method('lookup', topic).take_option_string()


def topics() -> List[str]:
    return method('topics').take_list_of_strings()


def completeTopic(topicPrefix: str) -> List[str]:
    return method('completeTopic', topicPrefix).take_list_of_strings()
