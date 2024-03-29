from dataclasses import dataclass
from typing import Any, List, Optional

from .. import ser
from ..lua import LuaNum
from ._base import BasePeripheral


__all__ = ('ModemMessage', 'WirelessModemPeripheral', 'WiredModemPeripheral')


@dataclass
class ModemMessage:
    reply_channel: int
    content: Any
    distance: LuaNum


class ModemMixin:
    def isOpen(self, channel: int) -> bool:
        return self._call(b'isOpen', channel).take_bool()

    def open(self, channel: int) -> None:
        return self._call(b'open', channel).take_none()

    def close(self, channel: int) -> None:
        return self._call(b'close', channel).take_none()

    def closeAll(self) -> None:
        return self._call(b'closeAll').take_none()

    def transmit(self, channel: int, replyChannel: int, message: Any) -> None:
        return self._call(b'transmit', channel, replyChannel, message).take_none()

    def isWireless(self) -> bool:
        return self._call(b'isWireless').take_bool()

    def receive(self, channel: int):
        from ..cc.os import captureEvent

        if self.isOpen(channel):
            raise Exception('Channel is busy')

        side = self._side.encode(ser._CC_ENC)
        self.open(channel)
        try:
            for evt in captureEvent('modem_message'):
                if evt[0] != side:
                    continue
                if evt[1] != channel:
                    continue
                yield ModemMessage(*evt[2:])
        finally:
            self.close(channel)


class WirelessModemPeripheral(BasePeripheral, ModemMixin):
    TYPE = 'modem'


class WiredModemPeripheral(BasePeripheral, ModemMixin):
    TYPE = 'modem'

    def getNameLocal(self) -> Optional[str]:
        return self._call(b'getNameLocal').take_option_string()

    def getNamesRemote(self) -> List[str]:
        return self._call(b'getNamesRemote').take_list_of_strings()

    def getTypeRemote(self, peripheralName: str) -> Optional[str]:
        return self._call(b'getTypeRemote', peripheralName).take_option_string()

    def isPresentRemote(self, peripheralName: str) -> bool:
        return self._call(b'isPresentRemote', peripheralName).take_bool()

    def wrapRemote(self, peripheralName: str) -> Optional[BasePeripheral]:
        # use instead getMethodsRemote and callRemote
        from ..cc.peripheral import wrap
        return wrap(peripheralName)
