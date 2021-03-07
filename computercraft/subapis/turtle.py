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


def craft(quantity: int = 64) -> bool:
    return method('craft', quantity).take_bool()


def forward() -> bool:
    return method('forward').take_bool()


def back() -> bool:
    return method('back').take_bool()


def up() -> bool:
    return method('up').take_bool()


def down() -> bool:
    return method('down').take_bool()


def turnLeft() -> bool:
    return method('turnLeft').take_bool()


def turnRight() -> bool:
    return method('turnRight').take_bool()


def select(slotNum: int) -> bool:
    return method('select', slotNum).take_bool()


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


def equipLeft() -> bool:
    return method('equipLeft').take_bool()


def equipRight() -> bool:
    return method('equipRight').take_bool()


def attack() -> bool:
    return method('attack').take_bool()


def attackUp() -> bool:
    return method('attackUp').take_bool()


def attackDown() -> bool:
    return method('attackDown').take_bool()


def dig() -> bool:
    return method('dig').take_bool()


def digUp() -> bool:
    return method('digUp').take_bool()


def digDown() -> bool:
    return method('digDown').take_bool()


def place(signText: str = None) -> bool:
    return method('place', ser.nil_encode(signText)).take_bool()


def placeUp(signText: str = None) -> bool:
    return method('placeUp', ser.nil_encode(signText)).take_bool()


def placeDown(signText: str = None) -> bool:
    return method('placeDown', ser.nil_encode(signText)).take_bool()


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


def drop(count: int = None) -> bool:
    return method('drop', count).take_bool()


def dropUp(count: int = None) -> bool:
    return method('dropUp', count).take_bool()


def dropDown(count: int = None) -> bool:
    return method('dropDown', count).take_bool()


def suck(amount: int = None) -> bool:
    return method('suck', amount).take_bool()


def suckUp(amount: int = None) -> bool:
    return method('suckUp', amount).take_bool()


def suckDown(amount: int = None) -> bool:
    return method('suckDown', amount).take_bool()


def refuel(quantity: int = None) -> bool:
    return method('refuel', quantity).take_bool()


def getFuelLevel() -> int:
    return method('getFuelLevel').take_int()


def getFuelLimit() -> int:
    return method('getFuelLimit').take_int()


def transferTo(slot: int, quantity: int = None) -> bool:
    return method('transferTo', slot, quantity).take_bool()
