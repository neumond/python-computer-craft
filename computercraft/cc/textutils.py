from typing import List, Union

from .. import ser
from ..lua import LuaNum
from ..sess import eval_lua


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
    return eval_lua(b'G:textutils:M:slowWrite', ser.cc_dirty_encode(text), rate).take_none()


def slowPrint(text: str, rate: LuaNum = None):
    return eval_lua(b'G:textutils:M:slowPrint', ser.cc_dirty_encode(text), rate).take_none()


def formatTime(time: LuaNum, twentyFourHour: bool = None) -> str:
    return eval_lua(b'G:textutils:M:formatTime', time, twentyFourHour).take_string()


def _prepareTab(rows_and_colors):
    r = []
    for item in rows_and_colors:
        if isinstance(item, int):
            r.append(item)
        else:
            r.append([ser.cc_dirty_encode(x) for x in item])
    return r


def tabulate(*rows_and_colors: Union[List[str], int]):
    return eval_lua(b'G:textutils:M:tabulate', *_prepareTab(rows_and_colors)).take_none()


def pagedTabulate(*rows_and_colors: Union[List[str], int]):
    return eval_lua(b'G:textutils:M:pagedTabulate', *_prepareTab(rows_and_colors)).take_none()


def pagedPrint(text: str, freeLines: int = None) -> int:
    return eval_lua(b'G:textutils:M:pagedPrint', ser.cc_dirty_encode(text), freeLines).take_int()


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
