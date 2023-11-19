from typing import Union


LuaTable = Union[list, dict]
LuaNum = Union[int, float]


class LuaExpr:
    def get_expr_code(self):
        raise NotImplementedError


class TempObject:
    def __init__(self, fid: bytes):
        self._fid = fid
