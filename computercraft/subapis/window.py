from contextlib import contextmanager
from typing import Tuple

from ..lua import lua_call
from ..rproc import nil, tuple2_integer, tuple3_string
from ..sess import eval_lua_method_factory, lua_context_object
from .base import BaseSubAPI
from .mixins import TermMixin, TermTarget


class CCWindow(BaseSubAPI, TermMixin):
    def setVisible(self, visibility: bool):
        return nil(self._method('setVisible', visibility))

    def redraw(self):
        return nil(self._method('redraw'))

    def restoreCursor(self):
        return nil(self._method('restoreCursor'))

    def getPosition(self) -> Tuple[int, int]:
        return tuple2_integer(self._method('getPosition'))

    def reposition(self, x: int, y: int, width: int = None, height: int = None, parent: TermTarget = None):
        return nil(self._method('reposition', x, y, width, height, parent))

    def getLine(self, y: int) -> Tuple[str, str, str]:
        return tuple3_string(self._method('getLine', y))

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
        lua_call('window.create', parentTerm, x, y, width, height, visible),
    ) as var:
        yield CCWindow(var)
