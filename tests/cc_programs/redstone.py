from cc import import_file, os, redstone

_lib = import_file('_lib.py', __file__)

assert set(redstone.getSides()) == {'top', 'bottom', 'front', 'back', 'left', 'right'}

_lib.step('Remove all the redstone from sides of computer')

side = 'top'

assert redstone.setOutput(side, True) is None
assert redstone.getOutput(side) is True
assert redstone.getAnalogOutput(side) == 15
assert redstone.setOutput(side, False) is None
assert redstone.getOutput(side) is False
assert redstone.getAnalogOutput(side) == 0

assert redstone.setAnalogOutput(side, 7) is None
assert redstone.getAnalogOutput(side) == 7
assert redstone.getOutput(side) is True
assert redstone.setAnalogOutput(side, 15) is None
assert redstone.getAnalogOutput(side) == 15
assert redstone.setAnalogOutput(side, 0) is None
assert redstone.getAnalogOutput(side) == 0
assert redstone.getOutput(side) is False

assert redstone.getInput(side) is False
assert redstone.getAnalogInput(side) == 0

_lib.step(f'Put redstone block on {side} side of computer')

assert redstone.getInput(side) is True
assert redstone.getAnalogInput(side) > 0

_lib.step(f'Remove redstone block\nPut piston on {side} side of computer')

assert redstone.getInput(side) is False
assert redstone.getAnalogInput(side) == 0
assert redstone.setOutput(side, True) is None
os.sleep(2)
assert redstone.setOutput(side, False) is None

print('Piston must have been activated\nRemove piston')

print('Test finished successfully')
