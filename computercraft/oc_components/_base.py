from uuid import UUID

from ..lua import LuaExpr
from ..sess import eval_lua


class BaseComponent(LuaExpr):
    TYPE = 'component'

    def __init__(self, address: UUID):
        self._addr = address

    @property
    def address(self):
        return self._addr

    def __str__(self):
        return '<Component {} {}>'.format(self.TYPE, self._addr)

    def _call(self, method, *args):
        return eval_lua(b'R:component:M:invoke', self._addr, method, *args)

    def get_expr_code(self):
        return b'component.proxy("' + str(self._addr).encode('ascii') + b'")'
