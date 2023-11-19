from typing import List

from ..sess import eval_lua


__all__ = (
    'parseImage',
    'loadImage',
    'drawPixel',
    'drawLine',
    'drawBox',
    'drawFilledBox',
    'drawImage',
)


def parseImage(data: bytes) -> List[List[int]]:
    return eval_lua(b'G:paintutils:M:parseImage', data).take_2d_int()


def loadImage(path: str) -> List[List[int]]:
    return eval_lua(b'G:paintutils:M:loadImage', path).take_2d_int()


def drawPixel(x: int, y: int, color: int = None):
    return eval_lua(b'G:paintutils:M:drawPixel', x, y, color).take_none()


def drawLine(startX: int, startY: int, endX: int, endY: int, color: int = None):
    return eval_lua(b'G:paintutils:M:drawLine', startX, startY, endX, endY, color).take_none()


def drawBox(startX: int, startY: int, endX: int, endY: int, color: int = None):
    return eval_lua(b'G:paintutils:M:drawBox', startX, startY, endX, endY, color).take_none()


def drawFilledBox(startX: int, startY: int, endX: int, endY: int, color: int = None):
    return eval_lua(b'G:paintutils:M:drawFilledBox', startX, startY, endX, endY, color).take_none()


def drawImage(image: List[List[int]], xPos: int, yPos: int):
    return eval_lua(b'G:paintutils:M:drawImage', image, xPos, yPos).take_none()
