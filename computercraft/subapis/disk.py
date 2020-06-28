from typing import Optional, Union

from .base import BaseSubAPI
from ..rproc import boolean, string, nil, option_integer, option_string, fact_option, fact_union


option_string_bool = fact_option(fact_union(
    (
        lambda v: v is True or v is False,
        boolean,
    ),
    pelse=string,
))


class DiskAPI(BaseSubAPI):
    _API = 'disk'

    async def isPresent(self, side: str) -> bool:
        return boolean(await self._send('isPresent', side))

    async def hasData(self, side: str) -> bool:
        return boolean(await self._send('hasData', side))

    async def getMountPath(self, side: str) -> Optional[str]:
        return option_string(await self._send('getMountPath', side))

    async def setLabel(self, side: str, label: str):
        return nil(await self._send('setLabel', side, label))

    async def getLabel(self, side: str) -> Optional[str]:
        return option_string(await self._send('getLabel', side))

    async def getID(self, side: str) -> Optional[int]:
        return option_integer(await self._send('getID', side))

    async def hasAudio(self, side: str) -> bool:
        return boolean(await self._send('hasAudio', side))

    async def getAudioTitle(self, side: str) -> Optional[Union[bool, str]]:
        return option_string_bool(await self._send('getAudioTitle', side))

    async def playAudio(self, side: str):
        return nil(await self._send('playAudio', side))

    async def stopAudio(self, side: str):
        return nil(await self._send('stopAudio', side))

    async def eject(self, side: str):
        return nil(await self._send('eject', side))
