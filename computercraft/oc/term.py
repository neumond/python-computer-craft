from typing import Tuple, Optional
from uuid import UUID

from .. import ser
from ..sess import eval_lua


__all__ = (
    'isAvailable',
    'getViewport',
    'getCursor',
    'setCursor',
    'getCursorBlink',
    'setCursorBlink',
    'clear',
    'clearLine',
    'read',
    'write',
    'screen',
    'keyboard',
)


def isAvailable() -> bool:
    return eval_lua(b'R:term:M:isAvailable').take_bool()


def getViewport() -> Tuple[int, int, int, int, int, int]:
    r = eval_lua(b'R:term:M:getViewport')
    return tuple(r.take_rounded_int() for _ in range(6))


def getCursor() -> Tuple[int, int]:
    r = eval_lua(b'R:term:M:getCursor')
    return tuple(r.take_rounded_int() for _ in range(2))


def setCursor(col: int, row: int) -> None:
    return eval_lua(b'R:term:M:setCursor', col, row).take_none()


def getCursorBlink() -> bool:
    return eval_lua(b'R:term:M:getCursorBlink').take_bool()


def setCursorBlink(enabled: bool) -> None:
    return eval_lua(b'R:term:M:setCursorBlink', enabled).take_none()


def clear() -> None:
    return eval_lua(b'R:term:M:clear').take_none()


def clearLine() -> None:
    return eval_lua(b'R:term:M:clearLine').take_none()


def read(dobreak: bool = True, pwchar: Optional[str] = None) -> [str, None, False]:
    r = eval_lua(
        b'R:term:M:read',
        None,  # TODO: history: table
        dobreak,
        None,  # TODO: hint:table or function
        ser.u_encode(pwchar))
    x = r.peek()
    if x is None or x is False:
        return x
    return r.take_unicode()


def write(value: str, wrap: bool = False) -> None:
    return eval_lua(
        b'R:term:M:write',
        ser.u_encode(value),
        wrap,
    ).take_none()


def screen() -> UUID:
    return eval_lua(b'R:term:M:screen').take_uuid()


def keyboard() -> UUID:
    return eval_lua(b'R:term:M:keyboard').take_uuid()


# TODO: term.gpu(): table
# TODO: term.pull([...]): ...
# TODO: term.bind(gpu)
