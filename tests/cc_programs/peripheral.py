from cc import import_file, peripheral

_lib = import_file('_lib.py', __file__)

_lib.step('Remove all peripherals')

side = 'top'

assert peripheral.getNames() == []
assert peripheral.getType(side) is None
assert peripheral.isPresent(side) is False
assert peripheral.wrap(side) is None

_lib.step(f'Put disk drive on {side} side of computer')

assert peripheral.getNames() == [side]
assert peripheral.getType(side) == 'drive'
assert peripheral.isPresent(side) is True
d = peripheral.wrap(side)
assert d is not None
assert d.isDiskPresent() is False

print('Test finished successfully')
