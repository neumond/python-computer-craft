from typing import Optional

from ._base import BasePeripheral


__all__ = ('ComputerPeripheral', 'TurtlePeripheral')


class ComputerMixin:
    def turnOn(self) -> None:
        return self._method(b'turnOn').take_none()

    def shutdown(self) -> None:
        return self._method(b'shutdown').take_none()

    def reboot(self) -> None:
        return self._method(b'reboot').take_none()

    def getID(self) -> int:
        return self._method(b'getID').take_int()

    def getLabel(self) -> Optional[str]:
        return self._method(b'getLabel').take_option_string()

    def isOn(self) -> bool:
        return self._method(b'isOn').take_bool()


class ComputerPeripheral(BasePeripheral, ComputerMixin):
    TYPE = 'computer'


class TurtlePeripheral(BasePeripheral, ComputerMixin):
    TYPE = 'turtle'
