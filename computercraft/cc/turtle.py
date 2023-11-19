from typing import Optional

from ..errors import LuaException
from ..sess import eval_lua


def inspect_result(rp):
    success = rp.take_bool()
    if not success:
        msg = rp.take_string()
        if msg == 'No block to inspect':
            return None
        raise LuaException(msg)
    return rp.take_dict()


def dig_result(rp):
    success = rp.take_bool()
    if not success:
        msg = rp.take_string()
        if msg == 'Nothing to dig here':
            return False
        raise LuaException(msg)
    return True


def suck_result(rp):
    success = rp.take_bool()
    if not success:
        msg = rp.take_string()
        if msg == 'No items to take':
            return False
        raise LuaException(msg)
    return True


def attack_result(rp):
    success = rp.take_bool()
    if not success:
        msg = rp.take_string()
        if msg == 'Nothing to attack here':
            return False
        raise LuaException(msg)
    return True


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


def craft(quantity: int = 64) -> None:
    return eval_lua(b'G:turtle:M:craft', quantity).check_bool_error()


def forward() -> None:
    return eval_lua(b'G:turtle:M:forward').check_bool_error()


def back() -> None:
    return eval_lua(b'G:turtle:M:back').check_bool_error()


def up() -> None:
    return eval_lua(b'G:turtle:M:up').check_bool_error()


def down() -> None:
    return eval_lua(b'G:turtle:M:down').check_bool_error()


def turnLeft() -> None:
    return eval_lua(b'G:turtle:M:turnLeft').check_bool_error()


def turnRight() -> None:
    return eval_lua(b'G:turtle:M:turnRight').check_bool_error()


def select(slotNum: int) -> None:
    return eval_lua(b'G:turtle:M:select', slotNum).check_bool_error()


def getSelectedSlot() -> int:
    return eval_lua(b'G:turtle:M:getSelectedSlot').take_int()


def getItemCount(slotNum: int = None) -> int:
    return eval_lua(b'G:turtle:M:getItemCount', slotNum).take_int()


def getItemSpace(slotNum: int = None) -> int:
    return eval_lua(b'G:turtle:M:getItemSpace', slotNum).take_int()


def getItemDetail(slotNum: int = None) -> Optional[dict]:
    rp = eval_lua(b'G:turtle:M:getItemDetail', slotNum)
    if rp.peek() is None:
        return None
    return rp.take_dict()


def equipLeft() -> None:
    return eval_lua(b'G:turtle:M:equipLeft').check_bool_error()


def equipRight() -> None:
    return eval_lua(b'G:turtle:M:equipRight').check_bool_error()


def attack() -> bool:
    return attack_result(eval_lua(b'G:turtle:M:attack'))


def attackUp() -> bool:
    return attack_result(eval_lua(b'G:turtle:M:attackUp'))


def attackDown() -> bool:
    return attack_result(eval_lua(b'G:turtle:M:attackDown'))


def dig() -> bool:
    return dig_result(eval_lua(b'G:turtle:M:dig'))


def digUp() -> bool:
    return dig_result(eval_lua(b'G:turtle:M:digUp'))


def digDown() -> bool:
    return dig_result(eval_lua(b'G:turtle:M:digDown'))


def place(signText: str = None) -> None:
    return eval_lua(b'G:turtle:M:place', signText).check_bool_error()


def placeUp(signText: str = None) -> None:
    return eval_lua(b'G:turtle:M:placeUp', signText).check_bool_error()


def placeDown(signText: str = None) -> None:
    return eval_lua(b'G:turtle:M:placeDown', signText).check_bool_error()


def detect() -> bool:
    return eval_lua(b'G:turtle:M:detect').take_bool()


def detectUp() -> bool:
    return eval_lua(b'G:turtle:M:detectUp').take_bool()


def detectDown() -> bool:
    return eval_lua(b'G:turtle:M:detectDown').take_bool()


def inspect() -> Optional[dict]:
    return inspect_result(eval_lua(b'G:turtle:M:inspect'))


def inspectUp() -> Optional[dict]:
    return inspect_result(eval_lua(b'G:turtle:M:inspectUp'))


def inspectDown() -> Optional[dict]:
    return inspect_result(eval_lua(b'G:turtle:M:inspectDown'))


def compare() -> bool:
    return eval_lua(b'G:turtle:M:compare').take_bool()


def compareUp() -> bool:
    return eval_lua(b'G:turtle:M:compareUp').take_bool()


def compareDown() -> bool:
    return eval_lua(b'G:turtle:M:compareDown').take_bool()


def compareTo(slot: int) -> bool:
    return eval_lua(b'G:turtle:M:compareTo', slot).take_bool()


def drop(count: int = None) -> None:
    return eval_lua(b'G:turtle:M:drop', count).check_bool_error()


def dropUp(count: int = None) -> None:
    return eval_lua(b'G:turtle:M:dropUp', count).check_bool_error()


def dropDown(count: int = None) -> None:
    return eval_lua(b'G:turtle:M:dropDown', count).check_bool_error()


def suck(amount: int = None) -> bool:
    return suck_result(eval_lua(b'G:turtle:M:suck', amount))


def suckUp(amount: int = None) -> bool:
    return suck_result(eval_lua(b'G:turtle:M:suckUp', amount))


def suckDown(amount: int = None) -> bool:
    return suck_result(eval_lua(b'G:turtle:M:suckDown', amount))


def refuel(quantity: int = None) -> None:
    return eval_lua(b'G:turtle:M:refuel', quantity).check_bool_error()


def getFuelLevel() -> int:
    return eval_lua(b'G:turtle:M:getFuelLevel').take_int()


def getFuelLimit() -> int:
    return eval_lua(b'G:turtle:M:getFuelLimit').take_int()


def transferTo(slot: int, quantity: int = None) -> None:
    return eval_lua(b'G:turtle:M:transferTo', slot, quantity).check_bool_error()
