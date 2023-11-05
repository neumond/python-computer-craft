from typing import Tuple

from .. import ser
from ._base import BasePeripheral


__all__ = ('PrinterPeripheral', )


class PrinterPeripheral(BasePeripheral):
    TYPE = 'printer'

    def newPage(self) -> bool:
        return self._call(b'newPage').take_bool()

    def endPage(self) -> bool:
        return self._call(b'endPage').take_bool()

    def write(self, text: str) -> None:
        return self._call(b'write', ser.cc_dirty_encode(text)).take_none()

    def setCursorPos(self, x: int, y: int) -> None:
        return self._call(b'setCursorPos', x, y).take_none()

    def getCursorPos(self) -> Tuple[int, int]:
        rp = self._call(b'getCursorPos')
        return tuple(rp.take_int() for _ in range(2))

    def getPageSize(self) -> Tuple[int, int]:
        rp = self._call(b'getPageSize')
        return tuple(rp.take_int() for _ in range(2))

    def setPageTitle(self, title: str) -> None:
        return self._call(b'setPageTitle', title).take_none()

    def getPaperLevel(self) -> int:
        return self._call(b'getPaperLevel').take_int()

    def getInkLevel(self) -> int:
        return self._call(b'getInkLevel').take_int()
