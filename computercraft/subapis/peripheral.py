from typing import Optional, List, Tuple, Any
from .base import (
    BaseSubAPI, bool_return, opt_str_return, list_return,
    nil_return, opt_int_return, int_return, str_return, bool_success,
)
from .mixins import TermMixin


class CCPeripheral(BaseSubAPI):
    def __init__(self, cc, call_fn):
        super().__init__(cc)
        self._send = call_fn


class CCDrive(CCPeripheral):
    async def isDiskPresent(self) -> bool:
        return bool_return(await self._send('isDiskPresent'))

    async def getDiskLabel(self) -> Optional[str]:
        return opt_str_return(await self._send('getDiskLabel'))

    async def setDiskLabel(self, label: str):
        return nil_return(await self._send('setDiskLabel', label))

    async def hasData(self) -> bool:
        return bool_return(await self._send('hasData'))

    async def getMountPath(self) -> Optional[str]:
        return opt_str_return(await self._send('getMountPath'))

    async def hasAudio(self) -> bool:
        return bool_return(await self._send('hasAudio'))

    async def getAudioTitle(self) -> Optional[str]:
        return opt_str_return(await self._send('getAudioTitle'))

    async def playAudio(self):
        return nil_return(await self._send('playAudio'))

    async def stopAudio(self):
        return nil_return(await self._send('stopAudio'))

    async def ejectDisk(self):
        return nil_return(await self._send('ejectDisk'))

    async def getDiskID(self) -> Optional[int]:
        return opt_int_return(await self._send('getDiskID'))


class CCMonitor(CCPeripheral, TermMixin):
    async def setTextScale(self, scale: int):
        return nil_return(await self._send('setTextScale', scale))


class CCComputer(CCPeripheral):
    async def turnOn(self):
        return nil_return(await self._send('turnOn'))

    async def shutdown(self):
        return nil_return(await self._send('shutdown'))

    async def reboot(self):
        return nil_return(await self._send('reboot'))

    async def getID(self) -> int:
        return int_return(await self._send('getID'))

    async def isOn(self) -> bool:
        return bool_return(await self._send('isOn'))


class CCModem(CCPeripheral):
    async def isOpen(self, channel: int) -> bool:
        return bool_return(await self._send('isOpen', channel))

    async def open(self, channel: int):
        return nil_return(await self._send('open', channel))

    async def close(self, channel: int):
        return nil_return(await self._send('close', channel))

    async def closeAll(self):
        return nil_return(await self._send('closeAll'))

    async def transmit(self, channel: int, replyChannel: int, message: Any):
        return nil_return(await self._send('transmit', channel, replyChannel, message))

    async def isWireless(self) -> bool:
        return bool_return(await self._send('isWireless'))

    # wired only functions below

    async def getNamesRemote(self) -> List[str]:
        return list_return(await self._send('getNamesRemote'))

    async def getTypeRemote(self, peripheralName: str) -> str:
        return str_return(await self._send('getTypeRemote', peripheralName))

    async def isPresentRemote(self, peripheralName: str) -> bool:
        return bool_return(await self._send('isPresentRemote', peripheralName))

    async def wrapRemote(self, peripheralName: str) -> CCPeripheral:
        # use instead getMethodsRemote and callRemote
        async def call_fn(method, *args):
            return await self._send('callRemote', peripheralName, method, *args)

        return TYPE_MAP[await self.getTypeRemote(peripheralName)](self._cc, call_fn)


class CCPrinter(CCPeripheral):
    async def newPage(self) -> bool:
        return bool_return(await self._send('newPage'))

    async def endPage(self) -> bool:
        return bool_return(await self._send('endPage'))

    async def write(self, text: str):
        return nil_return(await self._send('write', text))

    async def setCursorPos(self, x: int, y: int):
        return nil_return(await self._send('setCursorPos', x, y))

    async def getCursorPos(self) -> Tuple[int, int]:
        return tuple(await self._send('getCursorPos'))

    async def getPageSize(self) -> Tuple[int, int]:
        return tuple(await self._send('getPageSize'))

    async def setPageTitle(self, title: str):
        return nil_return(await self._send('setPageTitle', title))

    async def getPaperLevel(self) -> int:
        return int_return(await self._send('getPaperLevel'))

    async def getInkLevel(self) -> int:
        return int_return(await self._send('getInkLevel'))


class CCCommandBlock(CCPeripheral):
    async def getCommand(self) -> str:
        return str_return(await self._send('getCommand'))

    async def setCommand(self, command: str):
        return nil_return(await self._send('setCommand', command))

    async def runCommand(self):
        return bool_success(await self._send('runCommand'))


TYPE_MAP = {
    'drive': CCDrive,
    'monitor': CCMonitor,
    'computer': CCComputer,
    'modem': CCModem,
    'printer': CCPrinter,
    'command': CCCommandBlock,
}


class PeripheralAPI(BaseSubAPI):
    _API = 'peripheral'

    async def isPresent(self, side: str) -> bool:
        return bool_return(await self._send('isPresent', side))

    async def getType(self, side: str) -> Optional[str]:
        return opt_str_return(await self._send('getType', side))

    async def getNames(self) -> List[str]:
        return list_return(await self._send('getNames'))

    async def wrap(self, side: str) -> CCPeripheral:
        # use instead getMethods and call
        async def call_fn(method, *args):
            return await self._send('call', side, method, *args)

        return TYPE_MAP[await self.getType(side)](self._cc, call_fn)
