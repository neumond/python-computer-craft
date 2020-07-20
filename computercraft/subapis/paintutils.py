from typing import List

from ..sess import eval_lua_method_factory


method = eval_lua_method_factory('paintutils.')


__all__ = (
    'parseImage',
    'loadImage',
    'drawPixel',
    'drawLine',
    'drawBox',
    'drawFilledBox',
    'drawImage',
)


def parseImage(data: str) -> List[List[int]]:
    return method('parseImage', data).take_2d_int()


def loadImage(path: str) -> List[List[int]]:
    return method('loadImage', path).take_2d_int()


def drawPixel(x: int, y: int, color: int = None):
    return method('drawPixel', x, y, color).take_none()


def drawLine(startX: int, startY: int, endX: int, endY: int, color: int = None):
    return method('drawLine', startX, startY, endX, endY, color).take_none()


def drawBox(startX: int, startY: int, endX: int, endY: int, color: int = None):
    return method('drawBox', startX, startY, endX, endY, color).take_none()


def drawFilledBox(startX: int, startY: int, endX: int, endY: int, color: int = None):
    return method('drawFilledBox', startX, startY, endX, endY, color).take_none()


def drawImage(image: List[List[int]], xPos: int, yPos: int):
    return method('drawImage', image, xPos, yPos).take_none()
