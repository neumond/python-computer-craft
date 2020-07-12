from typing import Optional

from ..lua import lua_string
from ..rproc import option_integer, option_string
from ..sess import eval_lua, eval_lua_method_factory


method = eval_lua_method_factory('keys.')


__all__ = (
    'getCode',
    'getName',
)


def getCode(name: str) -> Optional[int]:
    # replaces properties
    # keys.space → keys.getCode('space')
    return option_integer(eval_lua('''
if type(keys[{key}]) == 'number' then
    return keys[{key}]
end
return nil'''.format(key=lua_string(name))))


def getName(code: int) -> Optional[str]:
    return option_string(method('getName', code))
