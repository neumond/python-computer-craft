from typing import Tuple, List, Optional

from ..rproc import tuple3_integer, any_dict, any_list, array_string, fact_tuple, boolean, option_integer
from ..sess import eval_lua_method_factory


command_result = fact_tuple(boolean, array_string, option_integer, tail_nils=1)
method = eval_lua_method_factory('commands.')


__all__ = (
    'exec',
    'list',
    'getBlockPosition',
    'getBlockInfo',
    'getBlockInfos',
)


def exec(command: str) -> Tuple[bool, List[str], Optional[int]]:
    return command_result(method('exec', command))


def list() -> List[str]:
    return array_string(method('list'))


def getBlockPosition() -> Tuple[int, int, int]:
    return tuple3_integer(method('getBlockPosition'))


def getBlockInfo(x: int, y: int, z: int) -> dict:
    return any_dict(method('getBlockInfo', x, y, z))


def getBlockInfos(x1: int, y1: int, z1: int, x2: int, y2: int, z2: int) -> List[dict]:
    return any_list(method('getBlockInfos', x1, y1, z1, x2, y2, z2))
