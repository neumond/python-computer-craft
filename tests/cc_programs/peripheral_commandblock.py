from cc import LuaException, import_file, peripheral

_lib = import_file('_lib.py', __file__)

side = 'left'

_lib.step(f'Attach command block at {side} side of computer')

m = peripheral.wrap(side)

assert m.getCommand() == ''
assert m.setCommand('say Hello from python side') is None
assert m.getCommand() == 'say Hello from python side'
assert m.runCommand() is None

assert m.setCommand('time query daytime') is None
assert m.getCommand() == 'time query daytime'
assert m.runCommand() is None

assert m.setCommand('') is None
assert m.getCommand() == ''
with _lib.assert_raises(LuaException):
    m.runCommand()

print('You must have seen chat message')
print('Test finished successfully')
