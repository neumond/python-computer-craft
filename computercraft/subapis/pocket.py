from ..rproc import flat_try_result
from ..sess import eval_lua_method_factory


method = eval_lua_method_factory('pocket.')


__all__ = (
    'equipBack',
    'unequipBack',
)


def equipBack():
    return flat_try_result(method('equipBack'))


def unequipBack():
    return flat_try_result(method('unequipBack'))
