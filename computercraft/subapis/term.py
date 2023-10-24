from typing import Tuple

from ..sess import eval_lua


__all__ = (
    'write',
    'blit',
    'clear',
    'clearLine',
    'getCursorPos',
    'setCursorPos',
    'getCursorBlink',
    'setCursorBlink',
    'isColor',
    'getSize',
    'scroll',
    'setTextColor',
    'getTextColor',
    'setBackgroundColor',
    'getBackgroundColor',
    'getPaletteColor',
    'setPaletteColor',
    'nativePaletteColor',
    # 'redirect',
    # 'get_current_target',
    # 'get_native_target',
)


def write(text: str) -> None:
    return eval_lua(b'G:term:M:write', text).take_none()


def blit(text: str, textColors: bytes, backgroundColors: bytes) -> None:
    return eval_lua(b'G:term:M:blit', text, textColors, backgroundColors).take_none()


def clear() -> None:
    return eval_lua(b'G:term:M:clear').take_none()


def clearLine() -> None:
    return eval_lua(b'G:term:M:clearLine').take_none()


def getCursorPos() -> Tuple[int, int]:
    rp = eval_lua(b'G:term:M:getCursorPos')
    return tuple(rp.take_int() for _ in range(2))


def setCursorPos(x: int, y: int) -> None:
    return eval_lua(b'G:term:M:setCursorPos', x, y).take_none()


def getCursorBlink() -> bool:
    return eval_lua(b'G:term:M:getCursorBlink').take_bool()


def setCursorBlink(value: bool):
    return eval_lua(b'G:term:M:setCursorBlink', value).take_none()


def isColor() -> bool:
    return eval_lua(b'G:term:M:isColor').take_bool()


def getSize() -> Tuple[int, int]:
    rp = eval_lua(b'G:term:M:getSize')
    return tuple(rp.take_int() for _ in range(2))


def scroll(lines: int) -> None:
    return eval_lua(b'G:term:M:scroll', lines).take_none()


def setTextColor(colorID: int) -> None:
    return eval_lua(b'G:term:M:setTextColor', colorID).take_none()


def getTextColor() -> int:
    return eval_lua(b'G:term:M:getTextColor').take_int()


def setBackgroundColor(colorID: int) -> None:
    return eval_lua(b'G:term:M:setBackgroundColor', colorID).take_none()


def getBackgroundColor() -> int:
    return eval_lua(b'G:term:M:getBackgroundColor').take_int()


def getPaletteColor(colorID: int) -> Tuple[float, float, float]:
    rp = eval_lua(b'G:term:M:getPaletteColor', colorID)
    return tuple(rp.take_number() for _ in range(3))


def setPaletteColor(colorID: int, r: float, g: float, b: float) -> None:
    return eval_lua(b'G:term:M:setPaletteColor', colorID, r, g, b).take_none()


def nativePaletteColor(colorID: int) -> Tuple[float, float, float]:
    rp = eval_lua(b'G:term:M:nativePaletteColor', colorID)
    return tuple(rp.take_number() for _ in range(3))


# @contextmanager
# def redirect(target: TermTarget):
#     with lua_context_object(
#         'term.redirect(...)',
#         (target, ),
#         'term.redirect({e})',
#     ):
#         yield


# def get_current_target() -> TermTarget:
#     return TermTarget('term.current()')


# def get_native_target() -> TermTarget:
#     return TermTarget('term.native()')
