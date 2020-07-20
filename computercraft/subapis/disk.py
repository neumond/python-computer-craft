from typing import Optional, Union

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
    return method('isPresent', side).take_bool()


def hasData(side: str) -> bool:
    return method('hasData', side).take_bool()


def getMountPath(side: str) -> Optional[str]:
    return method('getMountPath', side).take_option_string()


def setLabel(side: str, label: str):
    return method('setLabel', side, label).take_none()


def getLabel(side: str) -> Optional[str]:
    return method('getLabel', side).take_option_string()


def getID(side: str) -> Optional[int]:
    return method('getID', side).take_option_int()


def hasAudio(side: str) -> bool:
    return method('hasAudio', side).take_bool()


def getAudioTitle(side: str) -> Optional[Union[bool, str]]:
    return method('getAudioTitle', side).take_option_string_bool()


def playAudio(side: str):
    return method('playAudio', side).take_none()


def stopAudio(side: str):
    return method('stopAudio', side).take_none()


def eject(side: str):
    return method('eject', side).take_none()
