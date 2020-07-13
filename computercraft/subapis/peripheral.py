from dataclasses import dataclass
from typing import Optional, List, Tuple, Any, Union

from .mixins import TermMixin, TermTarget
from .turtle import craft_result
from ..lua import LuaNum, lua_args, return_lua_call
from ..rproc import (
    boolean, nil, integer, string, option_integer, option_string,
    tuple2_integer, array_string, option_string_bool, flat_try_result,
)
from ..sess import eval_lua, eval_lua_method_factory


class BasePeripheral:
    # NOTE: is not LuaExpr, you can't pass peripheral as parameter
    # TODO: to fix this we can supply separate lua expr, result of .wrap()

    def __init__(self, lua_method_expr, *prepend_params):
        self._lua_method_expr = lua_method_expr
        self._prepend_params = prepend_params

    def _method(self, name, *params):
        return eval_lua(return_lua_call(
            self._lua_method_expr,
            *self._prepend_params, name, *params,
        ))


class CCDrive(BasePeripheral):
    def isDiskPresent(self) -> bool:
        return boolean(self._method('isDiskPresent'))

    def getDiskLabel(self) -> Optional[str]:
        return option_string(self._method('getDiskLabel'))

    def setDiskLabel(self, label: str):
        return nil(self._method('setDiskLabel', label))

    def hasData(self) -> bool:
        return boolean(self._method('hasData'))

    def getMountPath(self) -> Optional[str]:
        return option_string(self._method('getMountPath'))

    def hasAudio(self) -> bool:
        return boolean(self._method('hasAudio'))

    def getAudioTitle(self) -> Optional[Union[bool, str]]:
        return option_string_bool(self._method('getAudioTitle'))

    def playAudio(self):
        return nil(self._method('playAudio'))

    def stopAudio(self):
        return nil(self._method('stopAudio'))

    def ejectDisk(self):
        return nil(self._method('ejectDisk'))

    def getDiskID(self) -> Optional[int]:
        return option_integer(self._method('getDiskID'))


class CCMonitor(BasePeripheral, TermMixin):
    def getTextScale(self) -> int:
        return integer(self._method('getTextScale'))

    def setTextScale(self, scale: int):
        return nil(self._method('setTextScale', scale))


class ComputerMixin:
    def turnOn(self):
        return nil(self._method('turnOn'))

    def shutdown(self):
        return nil(self._method('shutdown'))

    def reboot(self):
        return nil(self._method('reboot'))

    def getID(self) -> int:
        return integer(self._method('getID'))

    def getLabel(self) -> Optional[str]:
        return option_string(self._method('getLabel'))

    def isOn(self) -> bool:
        return boolean(self._method('isOn'))


class CCComputer(BasePeripheral, ComputerMixin):
    pass


class CCTurtle(BasePeripheral, ComputerMixin):
    pass


@dataclass
class ModemMessage:
    reply_channel: int
    content: Any
    distance: LuaNum


class ModemMixin:
    def isOpen(self, channel: int) -> bool:
        return boolean(self._method('isOpen', channel))

    def open(self, channel: int):
        return nil(self._method('open', channel))

    def close(self, channel: int):
        return nil(self._method('close', channel))

    def closeAll(self):
        return nil(self._method('closeAll'))

    def transmit(self, channel: int, replyChannel: int, message: Any):
        return nil(self._method('transmit', channel, replyChannel, message))

    def isWireless(self) -> bool:
        return boolean(self._method('isWireless'))

    @property
    def _side(self):
        return self._prepend_params[0]

    def receive(self, channel: int):
        from .os import pullEvent

        if self.isOpen(channel):
            raise Exception('Channel is busy')

        self.open(channel)
        try:
            while True:
                evt = pullEvent('modem_message')
                assert evt[0] == 'modem_message'
                if evt[1] != self._side:
                    continue
                if evt[2] != channel:
                    continue
                yield ModemMessage(*evt[3:])
        finally:
            self.close(channel)


class CCWirelessModem(BasePeripheral, ModemMixin):
    pass


class CCWiredModem(BasePeripheral, ModemMixin):
    def getNameLocal(self) -> Optional[str]:
        return option_string(self._method('getNameLocal'))

    def getNamesRemote(self) -> List[str]:
        return array_string(self._method('getNamesRemote'))

    def getTypeRemote(self, peripheralName: str) -> Optional[str]:
        return option_string(self._method('getTypeRemote', peripheralName))

    def isPresentRemote(self, peripheralName: str) -> bool:
        return boolean(self._method('isPresentRemote', peripheralName))

    def wrapRemote(self, peripheralName: str) -> Optional[BasePeripheral]:
        # use instead getMethodsRemote and callRemote
        # NOTE: you can also use peripheral.wrap(peripheralName)

        ptype = self.getTypeRemote(peripheralName)
        if ptype is None:
            return None

        return TYPE_MAP[ptype](
            self._lua_method_expr, *self._prepend_params,
            'callRemote', peripheralName,
        )

    # NOTE: for TermTarget use peripheral.get_term_target(peripheralName)


class CCPrinter(BasePeripheral):
    def newPage(self) -> bool:
        return boolean(self._method('newPage'))

    def endPage(self) -> bool:
        return boolean(self._method('endPage'))

    def write(self, text: str):
        return nil(self._method('write', text))

    def setCursorPos(self, x: int, y: int):
        return nil(self._method('setCursorPos', x, y))

    def getCursorPos(self) -> Tuple[int, int]:
        return tuple2_integer(self._method('getCursorPos'))

    def getPageSize(self) -> Tuple[int, int]:
        return tuple2_integer(self._method('getPageSize'))

    def setPageTitle(self, title: str):
        return nil(self._method('setPageTitle', title))

    def getPaperLevel(self) -> int:
        return integer(self._method('getPaperLevel'))

    def getInkLevel(self) -> int:
        return integer(self._method('getInkLevel'))


class CCSpeaker(BasePeripheral):
    def playNote(self, instrument: str, volume: int = 1, pitch: int = 1) -> bool:
        # instrument:
        # https://minecraft.gamepedia.com/Note_Block#Instruments
        # bass
        # basedrum
        # bell
        # chime
        # flute
        # guitar
        # hat
        # snare
        # xylophone
        # iron_xylophone
        # pling
        # banjo
        # bit
        # didgeridoo
        # cow_bell

        # volume 0..3
        # pitch 0..24
        return boolean(self._method('playNote', instrument, volume, pitch))

    def playSound(self, sound: str, volume: int = 1, pitch: int = 1):
        # volume 0..3
        # pitch 0..2
        return boolean(self._method('playSound', sound, volume, pitch))


class CCCommandBlock(BasePeripheral):
    def getCommand(self) -> str:
        return string(self._method('getCommand'))

    def setCommand(self, command: str):
        return nil(self._method('setCommand', command))

    def runCommand(self):
        return flat_try_result(self._method('runCommand'))


class CCWorkbench(BasePeripheral):
    def craft(self, quantity: int = 64) -> bool:
        return craft_result(self._method('craft', quantity))


TYPE_MAP = {
    'drive': CCDrive,
    'monitor': CCMonitor,
    'computer': CCComputer,
    'turtle': CCTurtle,
    'printer': CCPrinter,
    'speaker': CCSpeaker,
    'command': CCCommandBlock,
    'workbench': CCWorkbench,
}


method = eval_lua_method_factory('peripheral.')


__all__ = (
    'isPresent',
    'getType',
    'getNames',
    'wrap',
    'get_term_target',
)


def isPresent(side: str) -> bool:
    return boolean(method('isPresent', side))


def getType(side: str) -> Optional[str]:
    return option_string(method('getType', side))


def getNames() -> List[str]:
    return array_string(method('getNames'))


# use instead getMethods and call
def wrap(side: str) -> Optional[BasePeripheral]:
    ptype = getType(side)
    if ptype is None:
        return None

    m = 'peripheral.call'

    if ptype == 'modem':
        if boolean(method('call', side, 'isWireless')):
            return CCWirelessModem(m, side)
        else:
            return CCWiredModem(m, side)
    else:
        return TYPE_MAP[ptype](m, side)


def get_term_target(side: str) -> TermTarget:
    return TermTarget('peripheral.wrap({})'.format(
        lua_args(side),
    ))
