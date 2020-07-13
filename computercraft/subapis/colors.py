from typing import Tuple

from ..rproc import boolean, integer, tuple3_number
from ..sess import eval_lua_method_factory


method = eval_lua_method_factory('colors.')


__all__ = (
    'white',
    'orange',
    'magenta',
    'lightBlue',
    'yellow',
    'lime',
    'pink',
    'gray',
    'lightGray',
    'cyan',
    'purple',
    'blue',
    'brown',
    'green',
    'red',
    'black',
    'combine',
    'subtract',
    'test',
    'packRGB',
    'unpackRGB',
    'chars',
    'iter_colors',
)


white = 0x1
orange = 0x2
magenta = 0x4
lightBlue = 0x8
yellow = 0x10
lime = 0x20
pink = 0x40
gray = 0x80
lightGray = 0x100
cyan = 0x200
purple = 0x400
blue = 0x800
brown = 0x1000
green = 0x2000
red = 0x4000
black = 0x8000


# combine, subtract and test are mostly for redstone.setBundledOutput

def combine(*colors: int) -> int:
    return integer(method('combine', *colors))


def subtract(color_set: int, *colors: int) -> int:
    return integer(method('subtract', color_set, *colors))


def test(colors: int, color: int) -> bool:
    return boolean(method('test', colors, color))


def packRGB(r: float, g: float, b: float) -> int:
    return integer(method('packRGB', r, g, b))


def unpackRGB(rgb: int) -> Tuple[float, float, float]:
    return tuple3_number(method('unpackRGB', rgb))


# use these chars for term.blit
chars = {
    '0': white,
    '1': orange,
    '2': magenta,
    '3': lightBlue,
    '4': yellow,
    '5': lime,
    '6': pink,
    '7': gray,
    '8': lightGray,
    '9': cyan,
    'a': purple,
    'b': blue,
    'c': brown,
    'd': green,
    'e': red,
    'f': black,
}


def iter_colors():
    for c in chars.values():
        yield c
