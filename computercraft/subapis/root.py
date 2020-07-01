from ..lua import lua_args
from ..rproc import nil, boolean, string


class RootAPIMixin:
    async def print(self, *args):
        return nil(await self.eval_coro('print({})'.format(lua_args(*args))))

    async def read_line(self) -> str:
        return string(await self.eval_coro('return io.read()'))

    async def has_commands_api(self) -> bool:
        return boolean(await self.eval_coro('return commands ~= nil'))

    async def has_multishell_api(self) -> bool:
        return boolean(await self.eval_coro('return multishell ~= nil'))

    async def has_turtle_api(self) -> bool:
        return boolean(await self.eval_coro('return turtle ~= nil'))

    async def is_pocket(self) -> bool:
        return boolean(await self.eval_coro('return pocket ~= nil'))
