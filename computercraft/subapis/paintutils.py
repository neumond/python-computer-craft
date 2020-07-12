from typing import List

from ..rproc import nil, integer, fact_array
from ..sess import eval_lua_method_factory


array_2d_integer = fact_array(fact_array(integer))
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
    return array_2d_integer(method('parseImage', data))


def loadImage(path: str) -> List[List[int]]:
    return array_2d_integer(method('loadImage', path))


def drawPixel(x: int, y: int, color: int = None):
    return nil(method('drawPixel', x, y, color))


def drawLine(startX: int, startY: int, endX: int, endY: int, color: int = None):
    return nil(method('drawLine', startX, startY, endX, endY, color))


def drawBox(startX: int, startY: int, endX: int, endY: int, color: int = None):
    return nil(method('drawBox', startX, startY, endX, endY, color))


def drawFilledBox(startX: int, startY: int, endX: int, endY: int, color: int = None):
    return nil(method('drawFilledBox', startX, startY, endX, endY, color))


def drawImage(image: List[List[int]], xPos: int, yPos: int):
    return nil(method('drawImage', image, xPos, yPos))
