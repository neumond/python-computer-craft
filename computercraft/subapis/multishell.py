from typing import Optional

from ..rproc import integer, nil, boolean, option_string
from ..sess import eval_lua_method_factory


method = eval_lua_method_factory('multishell.')


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
    return integer(method('getCurrent'))


def getCount() -> int:
    return integer(method('getCount'))


def launch(environment: dict, programPath: str, *args: str) -> int:
    return integer(method('launch', environment, programPath, *args))


def setTitle(tabID: int, title: str):
    return nil(method('setTitle', tabID, title))


def getTitle(tabID: int) -> Optional[str]:
    return option_string(method('getTitle', tabID))


def setFocus(tabID: int) -> bool:
    return boolean(method('setFocus', tabID))


def getFocus() -> int:
    return integer(method('getFocus'))
