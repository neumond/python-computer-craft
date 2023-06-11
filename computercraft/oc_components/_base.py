from ..lua import LuaExpr
from ..sess import eval_lua


class BaseComponent(LuaExpr):
    def __init__(self, address: str):
        self._addr = address.encode('utf-8')

    def _call(self, method, *args):
        return eval_lua(b'R:component:M:invoke', self._addr, method, *args)

    def get_expr_code(self):
        return b'component.proxy("' + self._addr + b'")'
