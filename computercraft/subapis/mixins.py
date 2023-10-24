from typing import Tuple

from .. import ser
from ..lua import LuaExpr


class TermMixin:
    def write(self, text: str):
        return self._method(b'write', ser.dirty_encode(text)).take_none()

    def blit(self, text: str, textColors: bytes, backgroundColors: bytes):
        return self._method(b'blit', ser.dirty_encode(text), textColors, backgroundColors).take_none()

    def clear(self):
        return self._method(b'clear').take_none()

    def clearLine(self):
        return self._method(b'clearLine').take_none()

    def getCursorPos(self) -> Tuple[int, int]:
        rp = self._method(b'getCursorPos')
        return tuple(rp.take_int() for _ in range(2))

    def setCursorPos(self, x: int, y: int):
        return self._method(b'setCursorPos', x, y).take_none()

    def getCursorBlink(self) -> bool:
        return self._method(b'getCursorBlink').take_bool()

    def setCursorBlink(self, value: bool):
        return self._method(b'setCursorBlink', value).take_none()

    def isColor(self) -> bool:
        return self._method(b'isColor').take_bool()

    def getSize(self) -> Tuple[int, int]:
        rp = self._method(b'getSize')
        return tuple(rp.take_int() for _ in range(2))

    def scroll(self, lines: int):
        return self._method(b'scroll', lines).take_none()

    def setTextColor(self, colorID: int):
        return self._method(b'setTextColor', colorID).take_none()

    def getTextColor(self) -> int:
        return self._method(b'getTextColor').take_int()

    def setBackgroundColor(self, colorID: int):
        return self._method(b'setBackgroundColor', colorID).take_none()

    def getBackgroundColor(self) -> int:
        return self._method(b'getBackgroundColor').take_int()

    def getPaletteColor(self, colorID: int) -> Tuple[float, float, float]:
        rp = self._method(b'getPaletteColor', colorID)
        return tuple(rp.take_number() for _ in range(3))

    def setPaletteColor(self, colorID: int, r: float, g: float, b: float):
        return self._method(b'setPaletteColor', colorID, r, g, b).take_none()


class TermTarget(LuaExpr):
    def __init__(self, code):
        self._code = code

    def get_expr_code(self):
        return self._code
