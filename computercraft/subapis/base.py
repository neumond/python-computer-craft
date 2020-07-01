from ..lua import LuaExpr, lua_args


class BaseSubAPI(LuaExpr):
    def __init__(self, cc, lua_expr):
        self._cc = cc
        self._lua_expr = lua_expr

    def get_expr_code(self):
        return self._lua_expr

    async def _send(self, method, *params):
        return await self._method(method, *params)

    async def _method(self, name, *params):
        return await self._cc.eval_coro('return {}.{}({})'.format(
            self._lua_expr, name, lua_args(*params),
        ))
