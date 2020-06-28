from .base import lua_args
from ..rproc import nil, boolean, string


class RootAPIMixin:
    async def print(self, *args):
        return nil(await self._send_cmd('print({})'.format(lua_args(*args))))

    async def read_line(self) -> str:
        return string(await self._send_cmd('return io.read()'))

    async def has_commands_api(self) -> bool:
        return boolean(await self._send_cmd('return commands ~= nil'))

    async def has_multishell_api(self) -> bool:
        return boolean(await self._send_cmd('return multishell ~= nil'))

    async def has_turtle_api(self) -> bool:
        return boolean(await self._send_cmd('return turtle ~= nil'))

    async def is_pocket(self) -> bool:
        return boolean(await self._send_cmd('return pocket ~= nil'))
