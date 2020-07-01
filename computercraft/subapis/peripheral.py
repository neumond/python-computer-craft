from contextlib import asynccontextmanager
from dataclasses import dataclass
from typing import Optional, List, Tuple, Any, Union

from .base import BaseSubAPI
from .mixins import TermMixin
from ..lua import LuaNum, lua_args
from ..rproc import (
    boolean, nil, integer, string, option_integer, option_string,
    tuple2_integer, array_string, option_string_bool, try_result,
)


class BasePeripheral:
    # NOTE: is not LuaExpr, you can't pass peripheral as parameter

    def __init__(self, cc, lua_method_expr, *prepend_params):
        self._cc = cc
        self._lua_method_expr = lua_method_expr
        self._prepend_params = prepend_params

    async def _send(self, method, *params):
        return await self._method(method, *params)

    async def _method(self, name, *params):
        return await self._cc.eval_coro('return {}({})'.format(
            self._lua_method_expr,
            lua_args(*self._prepend_params, name, *params),
        ))


class CCDrive(BasePeripheral):
    async def isDiskPresent(self) -> bool:
        return boolean(await self._send('isDiskPresent'))

    async def getDiskLabel(self) -> Optional[str]:
        return option_string(await self._send('getDiskLabel'))

    async def setDiskLabel(self, label: str):
        return nil(await self._send('setDiskLabel', label))

    async def hasData(self) -> bool:
        return boolean(await self._send('hasData'))

    async def getMountPath(self) -> Optional[str]:
        return option_string(await self._send('getMountPath'))

    async def hasAudio(self) -> bool:
        return boolean(await self._send('hasAudio'))

    async def getAudioTitle(self) -> Optional[Union[bool, str]]:
        return option_string_bool(await self._send('getAudioTitle'))

    async def playAudio(self):
        return nil(await self._send('playAudio'))

    async def stopAudio(self):
        return nil(await self._send('stopAudio'))

    async def ejectDisk(self):
        return nil(await self._send('ejectDisk'))

    async def getDiskID(self) -> Optional[int]:
        return option_integer(await self._send('getDiskID'))


class CCMonitor(BasePeripheral, TermMixin):
    async def getTextScale(self) -> int:
        return integer(await self._send('getTextScale'))

    async def setTextScale(self, scale: int):
        return nil(await self._send('setTextScale', scale))


class CCComputer(BasePeripheral):
    async def turnOn(self):
        return nil(await self._send('turnOn'))

    async def shutdown(self):
        return nil(await self._send('shutdown'))

    async def reboot(self):
        return nil(await self._send('reboot'))

    async def getID(self) -> int:
        return integer(await self._send('getID'))

    async def getLabel(self) -> Optional[str]:
        return option_string(await self._send('getLabel'))

    async def isOn(self) -> bool:
        return boolean(await self._send('isOn'))


@dataclass
class ModemMessage:
    reply_channel: int
    content: Any
    distance: LuaNum


class ModemMixin:
    async def isOpen(self, channel: int) -> bool:
        return boolean(await self._send('isOpen', channel))

    async def open(self, channel: int):
        return nil(await self._send('open', channel))

    async def close(self, channel: int):
        return nil(await self._send('close', channel))

    async def closeAll(self):
        return nil(await self._send('closeAll'))

    async def transmit(self, channel: int, replyChannel: int, message: Any):
        return nil(await self._send('transmit', channel, replyChannel, message))

    async def isWireless(self) -> bool:
        return boolean(await self._send('isWireless'))

    def _mk_recv_filter(self, channel):
        def filter(msg):
            if msg[0] != self._side:
                return False, None
            if msg[1] != channel:
                return False, None
            return True, ModemMessage(*msg[2:])
        return filter

    @asynccontextmanager
    async def receive(self, channel: int):
        if await self.isOpen(channel):
            raise Exception('Channel is busy')
        await self.open(channel)
        try:
            async with self._cc.os.captureEvent('modem_message') as q:
                q.filter = self._mk_recv_filter(channel)
                yield q
        finally:
            await self.close(channel)


class CCWirelessModem(BasePeripheral, ModemMixin):
    pass


class CCWiredModem(BasePeripheral, ModemMixin):
    async def getNameLocal(self) -> Optional[str]:
        return option_string(await self._send('getNameLocal'))

    async def getNamesRemote(self) -> List[str]:
        return array_string(await self._send('getNamesRemote'))

    async def getTypeRemote(self, peripheralName: str) -> Optional[str]:
        return option_string(await self._send('getTypeRemote', peripheralName))

    async def isPresentRemote(self, peripheralName: str) -> bool:
        return boolean(await self._send('isPresentRemote', peripheralName))

    async def wrapRemote(self, peripheralName: str) -> Optional[BasePeripheral]:
        # use instead getMethodsRemote and callRemote

        ptype = await self.getTypeRemote(peripheralName)
        if ptype is None:
            return None

        return TYPE_MAP[ptype](
            self._cc,
            self._lua_method_expr, *self._prepend_params,
            'callRemote', peripheralName,
        )


class CCPrinter(BasePeripheral):
    async def newPage(self) -> bool:
        return boolean(await self._send('newPage'))

    async def endPage(self) -> bool:
        return boolean(await self._send('endPage'))

    async def write(self, text: str):
        return nil(await self._send('write', text))

    async def setCursorPos(self, x: int, y: int):
        return nil(await self._send('setCursorPos', x, y))

    async def getCursorPos(self) -> Tuple[int, int]:
        return tuple2_integer(await self._send('getCursorPos'))

    async def getPageSize(self) -> Tuple[int, int]:
        return tuple2_integer(await self._send('getPageSize'))

    async def setPageTitle(self, title: str):
        return nil(await self._send('setPageTitle', title))

    async def getPaperLevel(self) -> int:
        return integer(await self._send('getPaperLevel'))

    async def getInkLevel(self) -> int:
        return integer(await self._send('getInkLevel'))


class CCSpeaker(BasePeripheral):
    async def playNote(self, instrument: str, volume: int = 1, pitch: int = 1) -> bool:
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
        return boolean(await self._send('playNote', instrument, volume, pitch))

    async def playSound(self, sound: str, volume: int = 1, pitch: int = 1):
        # volume 0..3
        # pitch 0..2
        return boolean(await self._send('playSound', sound, volume, pitch))


class CCCommandBlock(BasePeripheral):
    async def getCommand(self) -> str:
        return string(await self._send('getCommand'))

    async def setCommand(self, command: str):
        return nil(await self._send('setCommand', command))

    async def runCommand(self):
        return try_result(await self._send('runCommand'))


TYPE_MAP = {
    'drive': CCDrive,
    'monitor': CCMonitor,
    'computer': CCComputer,
    'printer': CCPrinter,
    'speaker': CCSpeaker,
    'command': CCCommandBlock,
}


class PeripheralAPI(BaseSubAPI):
    async def isPresent(self, side: str) -> bool:
        return boolean(await self._send('isPresent', side))

    async def getType(self, side: str) -> Optional[str]:
        return option_string(await self._send('getType', side))

    async def getNames(self) -> List[str]:
        return array_string(await self._send('getNames'))

    # use instead getMethods and call
    async def wrap(self, side: str) -> Optional[BasePeripheral]:
        ptype = await self.getType(side)
        if ptype is None:
            return None

        m = self.get_expr_code() + '.call'

        if ptype == 'modem':
            if boolean(await self._send('call', side, 'isWireless')):
                return CCWirelessModem(self._cc, m, side)
            else:
                return CCWiredModem(self._cc, m, side)
        else:
            return TYPE_MAP[ptype](self._cc, m, side)
