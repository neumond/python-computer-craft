import inspect
from typing import List, Optional, Type, TypeVar

from ..sess import eval_lua
from ..cc_peripherals import register_std_peripherals
from ..cc_peripherals._base import BasePeripheral


__all__ = (
    'UnknownPeripheralError',
    'isPresent',
    'getType',
    'getNames',
    'wrap',
    'registerType',
)


P = TypeVar('Peripheral')
type_map = {}


class UnknownPeripheralError(TypeError):
    pass


def isPresent(side: str) -> bool:
    return eval_lua(b'G:peripheral:M:isPresent', side).take_bool()


def getType(side: str) -> Optional[str]:
    return eval_lua(b'G:peripheral:M:getType', side).take_option_string()


def getNames() -> List[str]:
    return eval_lua(b'G:peripheral:M:getNames').take_list_of_strings()


# use instead getMethods and call
def wrap(side: str) -> Optional[BasePeripheral]:
    ptype = getType(side)
    if ptype is None:
        return None

    if ptype not in type_map:
        raise UnknownPeripheralError(ptype)

    cls = type_map[ptype]
    if inspect.isclass(cls):
        return cls(side)
    else:
        def _call(method, *args):
            return eval_lua(b'G:peripheral:M:call', side, method, *args)

        return cls(side, ptype, _call)


def registerType(peripheralType: str, pcls: Type[P]):
    type_map[peripheralType] = pcls


register_std_peripherals(registerType)
