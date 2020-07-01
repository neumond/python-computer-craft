from ..lua import lua_args


class BaseSubAPI:
    _API = NotImplemented

    def __init__(self, cc):
        self._cc = cc

    async def _send(self, method, *params, omit_nulls=True):
        return await self._cc.eval_coro('return {}.{}({})'.format(
            self._API, method, lua_args(*params, omit_nulls=omit_nulls)
        ))
