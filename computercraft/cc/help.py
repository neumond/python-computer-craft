from typing import Optional, List

from ..sess import eval_lua


__all__ = (
    'path',
    'setPath',
    'lookup',
    'topics',
    'completeTopic',
)


def path() -> str:
    return eval_lua(b'G:help:M:path').take_string()


def setPath(path: str) -> None:
    return eval_lua(b'G:help:M:setPath', path).take_none()


def lookup(topic: str) -> Optional[str]:
    return eval_lua(b'G:help:M:lookup', topic).take_option_string()


def topics() -> List[str]:
    return eval_lua(b'G:help:M:topics').take_list_of_strings()


def completeTopic(topicPrefix: str) -> List[str]:
    return eval_lua(b'G:help:M:completeTopic', topicPrefix).take_list_of_strings()
