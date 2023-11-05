from ..subapis.term import TermMixin
from ._base import BasePeripheral


__all__ = ('MonitorPeripheral', )


class MonitorPeripheral(BasePeripheral, TermMixin):
    TYPE = 'monitor'

    def getTextScale(self) -> int:
        return self._call(b'getTextScale').take_int()

    def setTextScale(self, scale: int) -> None:
        return self._call(b'setTextScale', scale).take_none()
