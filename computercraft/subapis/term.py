from contextlib import contextmanager
from typing import Tuple

from .. import ser
from ..sess import eval_lua, lua_context_object, ContextObject


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
    'redirect',
    # 'get_current_target',
    # 'get_native_target',
)


class TermMixin:
    def write(self, text: str) -> None:
        return self._call(b'write', ser.cc_dirty_encode(text)).take_none()

    def blit(self, text: str, textColors: bytes, backgroundColors: bytes) -> None:
        return self._call(b'blit', ser.cc_dirty_encode(text), textColors, backgroundColors).take_none()

    def clear(self) -> None:
        return self._call(b'clear').take_none()

    def clearLine(self) -> None:
        return self._call(b'clearLine').take_none()

    def getCursorPos(self) -> Tuple[int, int]:
        rp = self._call(b'getCursorPos')
        return tuple(rp.take_int() for _ in range(2))

    def setCursorPos(self, x: int, y: int) -> None:
        return self._call(b'setCursorPos', x, y).take_none()

    def getCursorBlink(self) -> bool:
        return self._call(b'getCursorBlink').take_bool()

    def setCursorBlink(self, value: bool) -> None:
        return self._call(b'setCursorBlink', value).take_none()

    def isColor(self) -> bool:
        return self._call(b'isColor').take_bool()

    def getSize(self) -> Tuple[int, int]:
        rp = self._call(b'getSize')
        return tuple(rp.take_int() for _ in range(2))

    def scroll(self, lines: int) -> None:
        return self._call(b'scroll', lines).take_none()

    def setTextColor(self, colorID: int) -> None:
        return self._call(b'setTextColor', colorID).take_none()

    def getTextColor(self) -> int:
        return self._call(b'getTextColor').take_int()

    def setBackgroundColor(self, colorID: int) -> None:
        return self._call(b'setBackgroundColor', colorID).take_none()

    def getBackgroundColor(self) -> int:
        return self._call(b'getBackgroundColor').take_int()

    def getPaletteColor(self, colorID: int) -> Tuple[float, float, float]:
        rp = self._call(b'getPaletteColor', colorID)
        return tuple(rp.take_number() for _ in range(3))

    def setPaletteColor(self, colorID: int, r: float, g: float, b: float) -> None:
        return self._call(b'setPaletteColor', colorID, r, g, b).take_none()


class TermTarget(ContextObject, TermMixin):
    pass


class _Proxy(TermMixin):
    def _call(self, method, *args):
        return eval_lua(b'G:term:M:' + method, *args)


_p = _Proxy()


write = _p.write
blit = _p.blit
clear = _p.clear
clearLine = _p.clearLine
getCursorPos = _p.getCursorPos
setCursorPos = _p.setCursorPos
getCursorBlink = _p.getCursorBlink
setCursorBlink = _p.setCursorBlink
isColor = _p.isColor
getSize = _p.getSize
scroll = _p.scroll
setTextColor = _p.setTextColor
getTextColor = _p.getTextColor
setBackgroundColor = _p.setBackgroundColor
getBackgroundColor = _p.getBackgroundColor
getPaletteColor = _p.getPaletteColor
setPaletteColor = _p.setPaletteColor


def nativePaletteColor(colorID: int) -> Tuple[float, float, float]:
    rp = eval_lua(b'G:term:M:nativePaletteColor', colorID)
    return tuple(rp.take_number() for _ in range(3))


@contextmanager
def redirect(target: TermTarget):
    with lua_context_object(
        b'term.redirect(...)',
        (target, ),
        b'term.redirect({e})',
    ):
        yield


# TODO: implement

# def get_current_target() -> TermTarget:
#     return TermTarget('term.current()')


# def get_native_target() -> TermTarget:
#     return TermTarget('term.native()')
