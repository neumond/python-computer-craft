from typing import Tuple, List, Optional

from .. import ser
from ..sess import eval_lua_method_factory


method = eval_lua_method_factory('commands.')


__all__ = (
    'exec',
    'list',
    'getBlockPosition',
    'getBlockInfo',
    'getBlockInfos',
)


def exec(command: str) -> Tuple[bool, List[str], Optional[int]]:
    rp = method('exec', ser.encode(command))
    success = rp.take_bool()
    log = rp.take_list_of_strings()
    n = rp.take_option_int()
    return success, log, n


def list() -> List[str]:
    return method('list').take_list_of_strings()


def getBlockPosition() -> Tuple[int, int, int]:
    rp = method('getBlockPosition')
    return tuple(rp.take_int() for _ in range(3))


def getBlockInfo(x: int, y: int, z: int) -> dict:
    return method('getBlockInfo', x, y, z).take_dict()


def getBlockInfos(x1: int, y1: int, z1: int, x2: int, y2: int, z2: int) -> List[dict]:
    return method('getBlockInfos', x1, y1, z1, x2, y2, z2).take_list()
