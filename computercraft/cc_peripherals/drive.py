from typing import Optional, Union

from ._base import BasePeripheral


__all__ = ('DrivePeripheral', )


class DrivePeripheral(BasePeripheral):
    TYPE = 'drive'

    def isDiskPresent(self) -> bool:
        return self._call(b'isDiskPresent').take_bool()

    def getDiskLabel(self) -> Optional[str]:
        return self._call(b'getDiskLabel').take_option_string()

    def setDiskLabel(self, label: Optional[str]) -> None:
        return self._call(b'setDiskLabel', label).take_none()

    def hasData(self) -> bool:
        return self._call(b'hasData').take_bool()

    def getMountPath(self) -> Optional[str]:
        return self._call(b'getMountPath').take_option_string()

    def hasAudio(self) -> bool:
        return self._call(b'hasAudio').take_bool()

    def getAudioTitle(self) -> Optional[Union[bool, str]]:
        return self._call(b'getAudioTitle').take_option_string_bool()

    def playAudio(self) -> None:
        return self._call(b'playAudio').take_none()

    def stopAudio(self) -> None:
        return self._call(b'stopAudio').take_none()

    def ejectDisk(self) -> None:
        return self._call(b'ejectDisk').take_none()

    def getDiskID(self) -> Optional[int]:
        return self._call(b'getDiskID').take_option_int()
