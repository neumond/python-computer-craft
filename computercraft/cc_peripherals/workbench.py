from ._base import BasePeripheral


__all__ = ('WorkbenchPeripheral', )


class WorkbenchPeripheral(BasePeripheral):
    TYPE = 'workbench'

    def craft(self, quantity: int = 64):
        return self._call(b'craft', quantity).check_bool_error()
