from typing import Tuple

from ._base import BaseComponent


class GPUComponent(BaseComponent):
    TYPE = 'gpu'

    def maxDepth(self) -> int:
        return self._call(b'maxDepth').take_int()

    def getDepth(self) -> int:
        return self._call(b'getDepth').take_int()

    def setDepth(self, bit: int) -> str:
        return self._call(b'setDepth').take_string()

    def maxResolution(self) -> Tuple[int, int]:
        return self._call(b'maxResolution').take_2d_int()

    def getResolution(self) -> Tuple[int, int]:
        return self._call(b'getResolution').take_2d_int()

    def setResolution(self, width: int, height: int) -> bool:
        return self._call(b'setResolution', width, height).take_bool()
