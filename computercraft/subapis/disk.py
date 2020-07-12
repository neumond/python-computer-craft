from typing import Optional, Union

from ..rproc import boolean, nil, option_integer, option_string, option_string_bool
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
    return boolean(method('isPresent', side))


def hasData(side: str) -> bool:
    return boolean(method('hasData', side))


def getMountPath(side: str) -> Optional[str]:
    return option_string(method('getMountPath', side))


def setLabel(side: str, label: str):
    return nil(method('setLabel', side, label))


def getLabel(side: str) -> Optional[str]:
    return option_string(method('getLabel', side))


def getID(side: str) -> Optional[int]:
    return option_integer(method('getID', side))


def hasAudio(side: str) -> bool:
    return boolean(method('hasAudio', side))


def getAudioTitle(side: str) -> Optional[Union[bool, str]]:
    return option_string_bool(method('getAudioTitle', side))


def playAudio(side: str):
    return nil(method('playAudio', side))


def stopAudio(side: str):
    return nil(method('stopAudio', side))


def eject(side: str):
    return nil(method('eject', side))
