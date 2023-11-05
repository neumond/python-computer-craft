from typing import Dict, Optional

from ._base import BasePeripheral


__all__ = ('InventoryPeripheral', )


class InventoryPeripheral(BasePeripheral):
    TYPE = 'inventory'

    def getItemDetail(self, slot: int) -> Optional[dict]:
        return self._call(b'getItemDetail', slot).take()

    def list(self) -> Dict[int, dict]:
        return self._call(b'list').take_dict()

    def pullItems(self, fromName: str, fromSlot: int, limit: int = None, toSlot: int = None) -> int:
        return self._call(b'pullItems', fromName, fromSlot, limit, toSlot).take_int()

    def pushItems(self, toName: str, fromSlot: int, limit: int = None, toSlot: int = None) -> int:
        return self._call(b'pushItems', toName, fromSlot, limit, toSlot).take_int()

    def size(self) -> int:
        return self._call(b'size').take_int()
