from ..sess import eval_lua


__all__ = (
    'equipBack',
    'unequipBack',
)


def equipBack():
    return eval_lua(b'G:pocket:M:equipBack').check_bool_error()


def unequipBack():
    return eval_lua(b'G:pocket:M:unequipBack').check_bool_error()
