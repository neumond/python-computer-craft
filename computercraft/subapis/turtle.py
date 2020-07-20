from typing import Optional

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


def boolean_with_error_exclusion(exclude_msg):
    def proc(rp):
        return rp.bool_error_exclude(exclude_msg)
    return proc


dig_result = boolean_with_error_exclusion('Nothing to dig here')
move_result = boolean_with_error_exclusion('Movement obstructed')
place_result = boolean_with_error_exclusion('Cannot place block here')
suck_result = boolean_with_error_exclusion('No items to take')
drop_result = boolean_with_error_exclusion('No items to drop')
transfer_result = boolean_with_error_exclusion('No space for items')
attack_result = boolean_with_error_exclusion('Nothing to attack here')
craft_result = boolean_with_error_exclusion('No matching recipes')


def always_true(rp):
    assert rp.take_bool() is True
    # return value is useless
    return None


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
    return craft_result(method('craft', quantity))


def forward() -> bool:
    return move_result(method('forward'))


def back() -> bool:
    return move_result(method('back'))


def up() -> bool:
    return move_result(method('up'))


def down() -> bool:
    return move_result(method('down'))


def turnLeft():
    return always_true(method('turnLeft'))


def turnRight():
    return always_true(method('turnRight'))


def select(slotNum: int):
    return always_true(method('select', slotNum))


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
    return always_true(method('equipLeft'))


def equipRight():
    return always_true(method('equipRight'))


def attack() -> bool:
    return attack_result(method('attack'))


def attackUp() -> bool:
    return attack_result(method('attackUp'))


def attackDown() -> bool:
    return attack_result(method('attackDown'))


def dig() -> bool:
    return dig_result(method('dig'))


def digUp() -> bool:
    return dig_result(method('digUp'))


def digDown() -> bool:
    return dig_result(method('digDown'))


def place(signText: str = None) -> bool:
    return place_result(method('place', signText))


def placeUp() -> bool:
    return place_result(method('placeUp'))


def placeDown() -> bool:
    return place_result(method('placeDown'))


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
    return drop_result(method('drop', count))


def dropUp(count: int = None) -> bool:
    return drop_result(method('dropUp', count))


def dropDown(count: int = None) -> bool:
    return drop_result(method('dropDown', count))


def suck(amount: int = None) -> bool:
    return suck_result(method('suck', amount))


def suckUp(amount: int = None) -> bool:
    return suck_result(method('suckUp', amount))


def suckDown(amount: int = None) -> bool:
    return suck_result(method('suckDown', amount))


def refuel(quantity: int = None):
    return method('refuel', quantity).check_bool_error()


def getFuelLevel() -> int:
    return method('getFuelLevel').take_int()


def getFuelLimit() -> int:
    return method('getFuelLimit').take_int()


def transferTo(slot: int, quantity: int = None) -> bool:
    return transfer_result(method('transferTo', slot, quantity))
