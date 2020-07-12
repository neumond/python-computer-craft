from typing import List, Union

from ..lua import LuaNum
from ..rproc import nil, string, integer
from ..sess import eval_lua_method_factory


method = eval_lua_method_factory('textutils.')


__all__ = (
    'slowWrite',
    'slowPrint',
    'formatTime',
    'tabulate',
    'pagedTabulate',
    'pagedPrint',
    'complete',
)


def slowWrite(text: str, rate: LuaNum = None):
    return nil(method('slowWrite', text, rate))


def slowPrint(text: str, rate: LuaNum = None):
    return nil(method('slowPrint', text, rate))


def formatTime(time: LuaNum, twentyFourHour: bool = None) -> str:
    return string(method('formatTime', time, twentyFourHour))


def tabulate(*rows_and_colors: Union[list, int]):
    return nil(method('tabulate', *rows_and_colors))


def pagedTabulate(*rows_and_colors: Union[list, int]):
    return nil(method('pagedTabulate', *rows_and_colors))


def pagedPrint(text: str, freeLines: int = None) -> int:
    return integer(method('pagedPrint', text, freeLines))


def complete(partial: str, possible: List[str]) -> List[str]:
    return [p[len(partial):] for p in possible if p.startswith(partial)]


# Questionable to implement
# serialize
# unserialize

# Will not implement, use pythonic equivalents
# serializeJSON
# unserializeJSON
# urlEncode
# json_null
# empty_json_array
