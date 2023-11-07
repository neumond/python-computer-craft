from typing import Optional

from ._base import BasePeripheral


__all__ = ('ComputerPeripheral', )


class ComputerPeripheral(BasePeripheral):
    TYPE = 'computer'

    def turnOn(self) -> None:
        return self._call(b'turnOn').take_none()

    def shutdown(self) -> None:
        return self._call(b'shutdown').take_none()

    def reboot(self) -> None:
        return self._call(b'reboot').take_none()

    def getID(self) -> int:
        return self._call(b'getID').take_int()

    def getLabel(self) -> Optional[str]:
        return self._call(b'getLabel').take_option_string()

    def isOn(self) -> bool:
        return self._call(b'isOn').take_bool()
