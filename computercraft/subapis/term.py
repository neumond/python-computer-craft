from contextlib import contextmanager
from typing import Tuple

from .base import BaseSubAPI
from .mixins import TermMixin, TermTarget
from ..sess import eval_lua_method_factory, lua_context_object


class TermAPI(BaseSubAPI, TermMixin):
    pass


method = eval_lua_method_factory('term.')
tapi = TermAPI('term')


__all__ = (
    'write',
    'blit',
    'clear',
    'clearLine',
    'getCursorPos',
    'setCursorPos',
    'getCursorBlink',
    'setCursorBlink',
    'isColor',
    'getSize',
    'scroll',
    'setTextColor',
    'getTextColor',
    'setBackgroundColor',
    'getBackgroundColor',
    'getPaletteColor',
    'setPaletteColor',
    'nativePaletteColor',
    'redirect',
    'get_current_target',
    'get_native_target',
)


write = tapi.write
blit = tapi.blit
clear = tapi.clear
clearLine = tapi.clearLine
getCursorPos = tapi.getCursorPos
setCursorPos = tapi.setCursorPos
getCursorBlink = tapi.getCursorBlink
setCursorBlink = tapi.setCursorBlink
isColor = tapi.isColor
getSize = tapi.getSize
scroll = tapi.scroll
setTextColor = tapi.setTextColor
getTextColor = tapi.getTextColor
setBackgroundColor = tapi.setBackgroundColor
getBackgroundColor = tapi.getBackgroundColor
getPaletteColor = tapi.getPaletteColor
setPaletteColor = tapi.setPaletteColor


def nativePaletteColor(colorID: int) -> Tuple[float, float, float]:
    rp = method('nativePaletteColor', colorID)
    return tuple(rp.take_number() for _ in range(3))


@contextmanager
def redirect(target: TermTarget):
    with lua_context_object(
        'term.redirect(...)',
        (target, ),
        'term.redirect({e})',
    ):
        yield


def get_current_target() -> TermTarget:
    return TermTarget('term.current()')


def get_native_target() -> TermTarget:
    return TermTarget('term.native()')
