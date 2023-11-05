from ..lua import LuaExpr
from ..sess import eval_lua


class BasePeripheral(LuaExpr):
    TYPE = 'peripheral'

    def __init__(self, side: str):
        self._side = side

    @property
    def side(self):
        return self._side

    def __str__(self):
        return '<Peripheral {} {}>'.format(self.TYPE, self._side)

    def _call(self, method, *args):
        return eval_lua(b'G:peripheral:M:call', self._side, method, *args)

    def get_expr_code(self):
        return b'peripheral.wrap("' + self._side.encode('ascii') + b'")'
