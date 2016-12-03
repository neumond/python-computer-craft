from typing import Optional
from .base import BaseSubAPI, nil_return, bool_return, opt_str_return, opt_int_return


class DiskAPI(BaseSubAPI):
    _API = 'disk'

    async def isPresent(self, side: str) -> bool:
        return bool_return(await self._send('isPresent', side))

    async def hasData(self, side: str) -> bool:
        return bool_return(await self._send('hasData', side))

    async def getMountPath(self, side: str) -> Optional[str]:
        return opt_str_return(await self._send('getMountPath', side))

    async def setLabel(self, side: str, label: str):
        return nil_return(await self._send('setLabel', side, label))

    async def getLabel(self, side: str) -> Optional[str]:
        return opt_str_return(await self._send('getLabel', side))

    async def getID(self, side: str) -> Optional[int]:
        return opt_int_return(await self._send('getID', side))

    async def hasAudio(self, side: str) -> bool:
        return bool_return(await self._send('hasAudio', side))

    async def getAudioTitle(self, side: str) -> Optional[str]:
        return opt_str_return(await self._send('getAudioTitle', side))

    async def playAudio(self, side: str):
        return nil_return(await self._send('playAudio', side))

    async def stopAudio(self, side: str):
        return nil_return(await self._send('stopAudio', side))

    async def eject(self, side: str):
        return nil_return(await self._send('eject', side))
