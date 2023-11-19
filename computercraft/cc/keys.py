from typing import Optional

from ..sess import eval_lua


__all__ = (
    'getCode',
    'getName',
)


def getCode(name: str) -> Optional[int]:
    # replaces properties
    # keys.space → keys.getCode('space')
    return eval_lua(b'''
local k = ...
if type(keys[k]) == 'number' then
    return keys[k]
end
return nil''', name).take_option_int()


def getName(code: int) -> Optional[str]:
    return eval_lua(b'G:keys:M:getName', code).take_option_string()
