from typing import Optional

from .base import BaseSubAPI
from ..errors import LuaException
from ..rproc import integer, boolean, fact_option, any_dict, flat_try_result


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


class TurtleAPI(BaseSubAPI):
    async def craft(self, quantity: int = 1) -> bool:
        return craft_result(await self._send('craft', quantity))

    async def forward(self) -> bool:
        return move_result(await self._send('forward'))

    async def back(self) -> bool:
        return move_result(await self._send('back'))

    async def up(self) -> bool:
        return move_result(await self._send('up'))

    async def down(self) -> bool:
        return move_result(await self._send('down'))

    async def turnLeft(self):
        return always_true(await self._send('turnLeft'))

    async def turnRight(self):
        return always_true(await self._send('turnRight'))

    async def select(self, slotNum: int):
        return always_true(await self._send('select', slotNum))

    async def getSelectedSlot(self) -> int:
        return integer(await self._send('getSelectedSlot'))

    async def getItemCount(self, slotNum: int = None) -> int:
        return integer(await self._send('getItemCount', slotNum))

    async def getItemSpace(self, slotNum: int = None) -> int:
        return integer(await self._send('getItemSpace', slotNum))

    async def getItemDetail(self, slotNum: int = None) -> dict:
        return option_any_dict(await self._send('getItemDetail', slotNum))

    async def equipLeft(self):
        return always_true(await self._send('equipLeft'))

    async def equipRight(self):
        return always_true(await self._send('equipRight'))

    async def attack(self) -> bool:
        return attack_result(await self._send('attack'))

    async def attackUp(self) -> bool:
        return attack_result(await self._send('attackUp'))

    async def attackDown(self) -> bool:
        return attack_result(await self._send('attackDown'))

    async def dig(self) -> bool:
        return dig_result(await self._send('dig'))

    async def digUp(self) -> bool:
        return dig_result(await self._send('digUp'))

    async def digDown(self) -> bool:
        return dig_result(await self._send('digDown'))

    async def place(self, signText: str = None) -> bool:
        return place_result(await self._send('place', signText))

    async def placeUp(self) -> bool:
        return place_result(await self._send('placeUp'))

    async def placeDown(self) -> bool:
        return place_result(await self._send('placeDown'))

    async def detect(self) -> bool:
        return boolean(await self._send('detect'))

    async def detectUp(self) -> bool:
        return boolean(await self._send('detectUp'))

    async def detectDown(self) -> bool:
        return boolean(await self._send('detectDown'))

    async def inspect(self) -> Optional[dict]:
        return inspect_result(await self._send('inspect'))

    async def inspectUp(self) -> Optional[dict]:
        return inspect_result(await self._send('inspectUp'))

    async def inspectDown(self) -> Optional[dict]:
        return inspect_result(await self._send('inspectDown'))

    async def compare(self) -> bool:
        return boolean(await self._send('compare'))

    async def compareUp(self) -> bool:
        return boolean(await self._send('compareUp'))

    async def compareDown(self) -> bool:
        return boolean(await self._send('compareDown'))

    async def compareTo(self, slot: int) -> bool:
        return boolean(await self._send('compareTo', slot))

    async def drop(self, count: int = None) -> bool:
        return drop_result(await self._send('drop', count))

    async def dropUp(self, count: int = None) -> bool:
        return drop_result(await self._send('dropUp', count))

    async def dropDown(self, count: int = None) -> bool:
        return drop_result(await self._send('dropDown', count))

    async def suck(self, amount: int = None) -> bool:
        return suck_result(await self._send('suck', amount))

    async def suckUp(self, amount: int = None) -> bool:
        return suck_result(await self._send('suckUp', amount))

    async def suckDown(self, amount: int = None) -> bool:
        return suck_result(await self._send('suckDown', amount))

    async def refuel(self, quantity: int = None):
        return flat_try_result(await self._send('refuel', quantity))

    async def getFuelLevel(self) -> int:
        return integer(await self._send('getFuelLevel'))

    async def getFuelLimit(self) -> int:
        return integer(await self._send('getFuelLimit'))

    async def transferTo(self, slot: int, quantity: int = None) -> bool:
        return transfer_result(await self._send('transferTo', slot, quantity))
