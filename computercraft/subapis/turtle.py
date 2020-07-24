from typing import Optional

from .. import ser
from ..errors import LuaException
from ..sess import eval_lua_method_factory


method = eval_lua_method_factory('turtle.')


def inspect_result(rp):
    success = rp.take_bool()
    if not success:
        msg = rp.take_string()
        if msg == 'No block to inspect':
            return None
        raise LuaException(msg)
    else:
        return rp.take_dict()


__all__ = (
    'craft',
    'forward',
    'back',
    'up',
    'down',
    'turnLeft',
    'turnRight',
    'select',
    'getSelectedSlot',
    'getItemCount',
    'getItemSpace',
    'getItemDetail',
    'equipLeft',
    'equipRight',
    'attack',
    'attackUp',
    'attackDown',
    'dig',
    'digUp',
    'digDown',
    'place',
    'placeUp',
    'placeDown',
    'detect',
    'detectUp',
    'detectDown',
    'inspect',
    'inspectUp',
    'inspectDown',
    'compare',
    'compareUp',
    'compareDown',
    'compareTo',
    'drop',
    'dropUp',
    'dropDown',
    'suck',
    'suckUp',
    'suckDown',
    'refuel',
    'getFuelLevel',
    'getFuelLimit',
    'transferTo',
)


def craft(quantity: int = 64):
    return method('craft', quantity).check_bool_error()


def forward():
    return method('forward').check_bool_error()


def back():
    return method('back').check_bool_error()


def up():
    return method('up').check_bool_error()


def down():
    return method('down').check_bool_error()


def turnLeft():
    return method('turnLeft').check_bool_error()


def turnRight():
    return method('turnRight').check_bool_error()


def select(slotNum: int):
    return method('select', slotNum).check_bool_error()


def getSelectedSlot() -> int:
    return method('getSelectedSlot').take_int()


def getItemCount(slotNum: int = None) -> int:
    return method('getItemCount', slotNum).take_int()


def getItemSpace(slotNum: int = None) -> int:
    return method('getItemSpace', slotNum).take_int()


def getItemDetail(slotNum: int = None) -> Optional[dict]:
    rp = method('getItemDetail', slotNum)
    if rp.peek() is None:
        return None
    return rp.take_dict()


def equipLeft():
    return method('equipLeft').check_bool_error()


def equipRight():
    return method('equipRight').check_bool_error()


def attack():
    return method('attack').check_bool_error()


def attackUp():
    return method('attackUp').check_bool_error()


def attackDown():
    return method('attackDown').check_bool_error()


def dig():
    return method('dig').check_bool_error()


def digUp():
    return method('digUp').check_bool_error()


def digDown():
    return method('digDown').check_bool_error()


def place(signText: str = None):
    return method('place', ser.nil_encode(signText)).check_bool_error()


def placeUp(signText: str = None):
    return method('placeUp', ser.nil_encode(signText)).check_bool_error()


def placeDown(signText: str = None):
    return method('placeDown', ser.nil_encode(signText)).check_bool_error()


def detect() -> bool:
    return method('detect').take_bool()


def detectUp() -> bool:
    return method('detectUp').take_bool()


def detectDown() -> bool:
    return method('detectDown').take_bool()


def inspect() -> Optional[dict]:
    return inspect_result(method('inspect'))


def inspectUp() -> Optional[dict]:
    return inspect_result(method('inspectUp'))


def inspectDown() -> Optional[dict]:
    return inspect_result(method('inspectDown'))


def compare() -> bool:
    return method('compare').take_bool()


def compareUp() -> bool:
    return method('compareUp').take_bool()


def compareDown() -> bool:
    return method('compareDown').take_bool()


def compareTo(slot: int) -> bool:
    return method('compareTo', slot).take_bool()


def drop(count: int = None):
    return method('drop', count).check_bool_error()


def dropUp(count: int = None):
    return method('dropUp', count).check_bool_error()


def dropDown(count: int = None):
    return method('dropDown', count).check_bool_error()


def suck(amount: int = None):
    return method('suck', amount).check_bool_error()


def suckUp(amount: int = None):
    return method('suckUp', amount).check_bool_error()


def suckDown(amount: int = None):
    return method('suckDown', amount).check_bool_error()


def refuel(quantity: int = None):
    return method('refuel', quantity).check_bool_error()


def getFuelLevel() -> int:
    return method('getFuelLevel').take_int()


def getFuelLimit() -> int:
    return method('getFuelLimit').take_int()


def transferTo(slot: int, quantity: int = None):
    return method('transferTo', slot, quantity).check_bool_error()
