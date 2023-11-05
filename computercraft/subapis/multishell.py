from typing import Optional

from ..sess import eval_lua


__all__ = (
    'getCurrent',
    'getCount',
    'launch',
    'setTitle',
    'getTitle',
    'setFocus',
    'getFocus',
)


def getCurrent() -> int:
    return eval_lua(b'G:multishell:M:getCurrent').take_int()


def getCount() -> int:
    return eval_lua(b'G:multishell:M:getCount').take_int()


def launch(environment: dict, programPath: str, *args: str) -> int:
    return eval_lua(b'G:multishell:M:launch', environment, programPath, *args).take_int()


def setTitle(tabID: int, title: str):
    return eval_lua(b'G:multishell:M:setTitle', tabID, title).take_none()


def getTitle(tabID: int) -> Optional[str]:
    return eval_lua(b'G:multishell:M:getTitle', tabID).take_option_string()


def setFocus(tabID: int) -> bool:
    return eval_lua(b'G:multishell:M:setFocus', tabID).take_bool()


def getFocus() -> int:
    return eval_lua(b'G:multishell:M:getFocus').take_int()
