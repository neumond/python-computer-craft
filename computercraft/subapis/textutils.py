from typing import List, Union

from ..lua import LuaNum
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
    return method('slowWrite', text, rate).take_none()


def slowPrint(text: str, rate: LuaNum = None):
    return method('slowPrint', text, rate).take_none()


def formatTime(time: LuaNum, twentyFourHour: bool = None) -> str:
    return method('formatTime', time, twentyFourHour).take_string()


def tabulate(*rows_and_colors: Union[list, int]):
    return method('tabulate', *rows_and_colors).take_none()


def pagedTabulate(*rows_and_colors: Union[list, int]):
    return method('pagedTabulate', *rows_and_colors).take_none()


def pagedPrint(text: str, freeLines: int = None) -> int:
    return method('pagedPrint', text, freeLines).take_int()


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
