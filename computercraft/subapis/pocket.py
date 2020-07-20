from ..sess import eval_lua_method_factory


method = eval_lua_method_factory('pocket.')


__all__ = (
    'equipBack',
    'unequipBack',
)


def equipBack():
    return method('equipBack').check_bool_error()


def unequipBack():
    return method('unequipBack').check_bool_error()
