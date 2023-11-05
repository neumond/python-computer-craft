from ._base import BasePeripheral


__all__ = ('CommandPeripheral', )


class CommandPeripheral(BasePeripheral):
    TYPE = 'command'

    def getCommand(self) -> str:
        return self._call(b'getCommand').take_string()

    def setCommand(self, command: str) -> None:
        return self._call(b'setCommand', command).take_none()

    def runCommand(self):
        return self._call(b'runCommand').check_bool_error()
