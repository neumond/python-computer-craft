from ..lua import LuaExpr, lua_args
from ..sess import eval_lua


class BaseSubAPI(LuaExpr):
    def __init__(self, lua_expr):
        self._lua_expr = lua_expr

    def get_expr_code(self):
        return self._lua_expr

    def _method(self, name, *params):
        return eval_lua('return {}.{}({})'.format(
            self.get_expr_code(), name, lua_args(*params),
        ))
