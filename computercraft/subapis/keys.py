from typing import Optional

from .. import ser
from ..sess import eval_lua, eval_lua_method_factory


method = eval_lua_method_factory('keys.')


__all__ = (
    'getCode',
    'getName',
)


def getCode(name: str) -> Optional[int]:
    # replaces properties
    # keys.space → keys.getCode('space')
    return eval_lua('''
local k = ...
if type(keys[k]) == 'number' then
    return keys[k]
end
return nil''', ser.encode(name)).take_option_int()


def getName(code: int) -> Optional[str]:
    return method('getName', code).take_option_string()
