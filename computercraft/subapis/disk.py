from typing import Optional, Union

from ..sess import eval_lua


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
    return eval_lua(b'G:disk:M:isPresent', side).take_bool()


def hasData(side: str) -> bool:
    return eval_lua(b'G:disk:M:hasData', side).take_bool()


def getMountPath(side: str) -> Optional[str]:
    return eval_lua(b'G:disk:M:getMountPath', side).take_option_string()


def setLabel(side: str, label: Optional[str]):
    return eval_lua(b'G:disk:M:setLabel', side, label).take_none()


def getLabel(side: str) -> Optional[str]:
    return eval_lua(b'G:disk:M:getLabel', side).take_option_string()


def getID(side: str) -> Optional[int]:
    return eval_lua(b'G:disk:M:getID', side).take_option_int()


def hasAudio(side: str) -> bool:
    return eval_lua(b'G:disk:M:hasAudio', side).take_bool()


def getAudioTitle(side: str) -> Optional[Union[bool, str]]:
    return eval_lua(b'G:disk:M:getAudioTitle', side).take_option_string_bool()


def playAudio(side: str):
    return eval_lua(b'G:disk:M:playAudio', side).take_none()


def stopAudio(side: str):
    return eval_lua(b'G:disk:M:stopAudio', side).take_none()


def eject(side: str):
    return eval_lua(b'G:disk:M:eject', side).take_none()
