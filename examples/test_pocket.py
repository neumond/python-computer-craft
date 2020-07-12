from cc import LuaException, import_file, pocket, peripheral

_lib = import_file('_lib.py', __file__)


assert peripheral.isPresent('back') is False

tbl = _lib.get_object_table('pocket')
assert _lib.get_class_table(pocket) == tbl

_lib.step('Clean inventory from any pocket upgrades')

with _lib.assert_raises(LuaException):
    pocket.equipBack()
with _lib.assert_raises(LuaException):
    pocket.unequipBack()
assert peripheral.isPresent('back') is False

_lib.step('Put any pocket upgrade to inventory')

assert pocket.equipBack() is None
assert peripheral.isPresent('back') is True

assert pocket.unequipBack() is None
assert peripheral.isPresent('back') is False

print('Test finished successfully')
