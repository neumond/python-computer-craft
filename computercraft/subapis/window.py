from contextlib import contextmanager
from typing import Tuple

from ..sess import eval_lua_method_factory, lua_context_object
from .base import BaseSubAPI
from .mixins import TermMixin, TermTarget


class CCWindow(BaseSubAPI, TermMixin):
    def setVisible(self, visibility: bool):
        return self._method('setVisible', visibility).take_none()

    def redraw(self):
        return self._method('redraw').take_none()

    def restoreCursor(self):
        return self._method('restoreCursor').take_none()

    def getPosition(self) -> Tuple[int, int]:
        rp = self._method('getPosition')
        return tuple(rp.take_int() for _ in range(2))

    def reposition(self, x: int, y: int, width: int = None, height: int = None, parent: TermTarget = None):
        return self._method('reposition', x, y, width, height, parent).take_none()

    def getLine(self, y: int) -> Tuple[str, str, str]:
        rp = self._method('getLine', y)
        return tuple(rp.take_string() for _ in range(3))

    def get_term_target(self) -> TermTarget:
        return TermTarget(self.get_expr_code())


method = eval_lua_method_factory('window.')


__all__ = (
    'create',
)


@contextmanager
def create(
    parentTerm: TermTarget, x: int, y: int, width: int, height: int, visible: bool = None,
) -> CCWindow:
    with lua_context_object(
        'window.create({}, ...)'.format(parentTerm.get_expr_code()),
        (x, y, width, height, visible),
    ) as var:
        yield CCWindow(var)
