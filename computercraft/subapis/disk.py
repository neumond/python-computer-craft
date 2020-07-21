from typing import Optional, Union

from .. import ser
from ..sess import eval_lua_method_factory


method = eval_lua_method_factory('disk.')


__all__ = (
    'isPresent',
    'hasData',
    'getMountPath',
    'setLabel',
    'getLabel',
    'getID',
    'hasAudio',
    'getAudioTitle',
    'playAudio',
    'stopAudio',
    'eject',
)


def isPresent(side: str) -> bool:
    return method('isPresent', ser.encode(side)).take_bool()


def hasData(side: str) -> bool:
    return method('hasData', ser.encode(side)).take_bool()


def getMountPath(side: str) -> Optional[str]:
    return method('getMountPath', ser.encode(side)).take_option_string()


def setLabel(side: str, label: Optional[str]):
    return method('setLabel', ser.encode(side), ser.nil_encode(label)).take_none()


def getLabel(side: str) -> Optional[str]:
    return method('getLabel', ser.encode(side)).take_option_string()


def getID(side: str) -> Optional[int]:
    return method('getID', ser.encode(side)).take_option_int()


def hasAudio(side: str) -> bool:
    return method('hasAudio', ser.encode(side)).take_bool()


def getAudioTitle(side: str) -> Optional[Union[bool, str]]:
    return method('getAudioTitle', ser.encode(side)).take_option_string_bool()


def playAudio(side: str):
    return method('playAudio', ser.encode(side)).take_none()


def stopAudio(side: str):
    return method('stopAudio', ser.encode(side)).take_none()


def eject(side: str):
    return method('eject', ser.encode(side)).take_none()
