from contextlib import asynccontextmanager
from typing import Tuple

from .base import BaseSubAPI
from .mixins import TermMixin, TermTarget
from ..lua import lua_args
from ..rproc import tuple3_number


class TermAPI(BaseSubAPI, TermMixin):
    async def nativePaletteColor(self, colorID: int) -> Tuple[float, float, float]:
        return tuple3_number(await self._send('nativePaletteColor', colorID))

    @asynccontextmanager
    async def redirect(self, target: TermTarget):
        create_expr = '{}.redirect({})'.format(
            self.get_expr_code(),
            lua_args(target),
        )
        fin_tpl = '{}.redirect({{e}})'.format(
            self.get_expr_code(),
        )
        async with self._cc._create_temp_object(create_expr, fin_tpl):
            yield

    def get_current_target(self) -> TermTarget:
        return TermTarget('{}.current()'.format(self.get_expr_code()))

    def get_native_target(self) -> TermTarget:
        return TermTarget('{}.native()'.format(self.get_expr_code()))
