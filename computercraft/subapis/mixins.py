from typing import Tuple

from ..lua import LuaExpr
from ..rproc import boolean, nil, integer, tuple3_number, tuple2_integer


class TermMixin:
    def write(self, text: str):
        return nil(self._method('write', text))

    def blit(self, text: str, textColors: str, backgroundColors: str):
        return nil(self._method('blit', text, textColors, backgroundColors))

    def clear(self):
        return nil(self._method('clear'))

    def clearLine(self):
        return nil(self._method('clearLine'))

    def getCursorPos(self) -> Tuple[int, int]:
        return tuple2_integer(self._method('getCursorPos'))

    def setCursorPos(self, x: int, y: int):
        return nil(self._method('setCursorPos', x, y))

    def getCursorBlink(self) -> bool:
        return boolean(self._method('getCursorBlink'))

    def setCursorBlink(self, value: bool):
        return nil(self._method('setCursorBlink', value))

    def isColor(self) -> bool:
        return boolean(self._method('isColor'))

    def getSize(self) -> Tuple[int, int]:
        return tuple2_integer(self._method('getSize'))

    def scroll(self, lines: int):
        return nil(self._method('scroll', lines))

    def setTextColor(self, colorID: int):
        return nil(self._method('setTextColor', colorID))

    def getTextColor(self) -> int:
        return integer(self._method('getTextColor'))

    def setBackgroundColor(self, colorID: int):
        return nil(self._method('setBackgroundColor', colorID))

    def getBackgroundColor(self) -> int:
        return integer(self._method('getBackgroundColor'))

    def getPaletteColor(self, colorID: int) -> Tuple[float, float, float]:
        return tuple3_number(self._method('getPaletteColor', colorID))

    def setPaletteColor(self, colorID: int, r: float, g: float, b: float):
        return nil(self._method('setPaletteColor', colorID, r, g, b))


class TermTarget(LuaExpr):
    def __init__(self, code):
        self._code = code

    def get_expr_code(self):
        return self._code
