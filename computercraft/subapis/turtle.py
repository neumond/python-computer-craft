from typing import Optional

from ..errors import LuaException
from ..rproc import integer, boolean, fact_option, any_dict, flat_try_result
from ..sess import eval_lua_method_factory


method = eval_lua_method_factory('turtle.')
option_any_dict = fact_option(any_dict)


def inspect_result(r):
    assert isinstance(r, list)
    assert len(r) == 2
    success, data = r
    assert isinstance(success, bool)
    if not success:
        if data == 'No block to inspect':
            return None
        raise LuaException(data)
    else:
        return any_dict(data)


def boolean_with_error_exclusion(exclude_msg):
    def proc(r):
        if r is True:
            return True
        assert isinstance(r, list)
        assert len(r) == 2
        success, msg = r
        assert isinstance(success, bool)
        if not success:
            if msg == exclude_msg:
                return False
            raise LuaException(msg)
        else:
            return True
    return proc


dig_result = boolean_with_error_exclusion('Nothing to dig here')
move_result = boolean_with_error_exclusion('Movement obstructed')
place_result = boolean_with_error_exclusion('Cannot place block here')
suck_result = boolean_with_error_exclusion('No items to take')
drop_result = boolean_with_error_exclusion('No items to drop')
transfer_result = boolean_with_error_exclusion('No space for items')
attack_result = boolean_with_error_exclusion('Nothing to attack here')
craft_result = boolean_with_error_exclusion('No matching recipes')


def always_true(r):
    assert boolean(r) is True
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
    return integer(method('getSelectedSlot'))


def getItemCount(slotNum: int = None) -> int:
    return integer(method('getItemCount', slotNum))


def getItemSpace(slotNum: int = None) -> int:
    return integer(method('getItemSpace', slotNum))


def getItemDetail(slotNum: int = None) -> dict:
    return option_any_dict(method('getItemDetail', slotNum))


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
    return boolean(method('detect'))


def detectUp() -> bool:
    return boolean(method('detectUp'))


def detectDown() -> bool:
    return boolean(method('detectDown'))


def inspect() -> Optional[dict]:
    return inspect_result(method('inspect'))


def inspectUp() -> Optional[dict]:
    return inspect_result(method('inspectUp'))


def inspectDown() -> Optional[dict]:
    return inspect_result(method('inspectDown'))


def compare() -> bool:
    return boolean(method('compare'))


def compareUp() -> bool:
    return boolean(method('compareUp'))


def compareDown() -> bool:
    return boolean(method('compareDown'))


def compareTo(slot: int) -> bool:
    return boolean(method('compareTo', slot))


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
    return flat_try_result(method('refuel', quantity))


def getFuelLevel() -> int:
    return integer(method('getFuelLevel'))


def getFuelLimit() -> int:
    return integer(method('getFuelLimit'))


def transferTo(slot: int, quantity: int = None) -> bool:
    return transfer_result(method('transferTo', slot, quantity))
