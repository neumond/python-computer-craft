def register_std_peripherals(register):
    from .command import CommandPeripheral
    from .computer import ComputerPeripheral, TurtlePeripheral
    from .drive import DrivePeripheral
    from .inventory import InventoryPeripheral
    from .modem import WirelessModemPeripheral, WiredModemPeripheral
    from .printer import PrinterPeripheral
    from .speaker import SpeakerPeripheral
    from .term import MonitorPeripheral
    from .workbench import WorkbenchPeripheral

    register('command', CommandPeripheral)
    register('computer', ComputerPeripheral)
    register('turtle', TurtlePeripheral)
    register('drive', DrivePeripheral)

    def _inv(side, ptype, call):
        p = InventoryPeripheral(side)
        p.TYPE = ptype
        return p

    for k in [
        'chest',
        'furnace',
        'barrel',
        'hopper',
        'dropper',
        'dispenser',
        'blast_furnace',
        'smoker',
        'shulker_box',
        'brewing_stand',
    ]:
        register('minecraft:' + k, _inv)

    def _modem(side, ptype, call):
        if call(b'isWireless').take_bool():
            return WirelessModemPeripheral(side)
        else:
            return WiredModemPeripheral(side)

    register('modem', _modem)
    register('printer', PrinterPeripheral)
    register('speaker', SpeakerPeripheral)
    register('monitor', MonitorPeripheral)
    register('workbench', WorkbenchPeripheral)
