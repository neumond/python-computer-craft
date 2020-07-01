from typing import Optional

from .base import BaseSubAPI
from ..lua import LuaNum
from ..errors import LuaException
from ..rproc import nil, integer, number, boolean, fact_option, any_dict


option_any_dict = fact_option(any_dict)


class TurtleAPI(BaseSubAPI):
    async def craft(self, quantity: int):
        return nil(await self._send('craft', quantity))

    async def forward(self):
        return nil(await self._send('forward'))

    async def back(self):
        return nil(await self._send('back'))

    async def up(self):
        return nil(await self._send('up'))

    async def down(self):
        return nil(await self._send('down'))

    async def turnLeft(self):
        return nil(await self._send('turnLeft'))

    async def turnRight(self):
        return nil(await self._send('turnRight'))

    async def select(self, slotNum: int):
        return nil(await self._send('select', slotNum))

    async def getSelectedSlot(self) -> int:
        return integer(await self._send('getSelectedSlot'))

    async def getItemCount(self, slotNum: int = None) -> int:
        return integer(await self._send('getItemCount', slotNum))

    async def getItemSpace(self, slotNum: int = None) -> int:
        return integer(await self._send('getItemSpace', slotNum))

    async def getItemDetail(self, slotNum: int = None) -> dict:
        return option_any_dict(await self._send('getItemDetail', slotNum))

    async def equipLeft(self):
        return nil(await self._send('equipLeft'))

    async def equipRight(self):
        return nil(await self._send('equipRight'))

    async def attack(self):
        return nil(await self._send('attack'))

    async def attackUp(self):
        return nil(await self._send('attackUp'))

    async def attackDown(self):
        return nil(await self._send('attackDown'))

    async def dig(self):
        return nil(await self._send('dig'))

    async def digUp(self):
        return nil(await self._send('digUp'))

    async def digDown(self):
        return nil(await self._send('digDown'))

    async def place(self, signText: str = None):
        return nil(await self._send('place', signText))

    async def placeUp(self):
        return nil(await self._send('placeUp'))

    async def placeDown(self):
        return nil(await self._send('placeDown'))

    async def detect(self) -> bool:
        return boolean(await self._send('detect'))

    async def detectUp(self) -> bool:
        return boolean(await self._send('detectUp'))

    async def detectDown(self) -> bool:
        return boolean(await self._send('detectDown'))

    async def _inspect(self, method):
        try:
            return any_dict(await self._send(method))
        except LuaException as e:
            if e.args == ('No block to inspect', ):
                return None
            raise e

    async def inspect(self) -> Optional[dict]:
        return self._inspect('inspect')

    async def inspectUp(self) -> Optional[dict]:
        return self._inspect('inspectUp')

    async def inspectDown(self) -> Optional[dict]:
        return self._inspect('inspectDown')

    async def compare(self) -> bool:
        return boolean(await self._send('compare'))

    async def compareUp(self) -> bool:
        return boolean(await self._send('compareUp'))

    async def compareDown(self) -> bool:
        return boolean(await self._send('compareDown'))

    async def compareTo(self, slot: int) -> bool:
        return boolean(await self._send('compareTo', slot))

    async def drop(self, count: LuaNum = None):
        return nil(await self._send('drop', count))

    async def dropUp(self, count: LuaNum = None):
        return nil(await self._send('dropUp', count))

    async def dropDown(self, count: LuaNum = None):
        return nil(await self._send('dropDown', count))

    async def suck(self, amount: LuaNum = None):
        return nil(await self._send('suck', amount))

    async def suckUp(self, amount: LuaNum = None):
        return nil(await self._send('suckUp', amount))

    async def suckDown(self, amount: LuaNum = None):
        return nil(await self._send('suckDown', amount))

    async def refuel(self, quantity: LuaNum = None):
        return nil(await self._send('refuel', quantity))

    async def getFuelLevel(self) -> LuaNum:
        return number(await self._send('getFuelLevel'))

    async def getFuelLimit(self) -> LuaNum:
        return number(await self._send('getFuelLimit'))

    async def transferTo(self, slot: int, quantity: int = None):
        return nil(await self._send('transferTo', slot, quantity))
