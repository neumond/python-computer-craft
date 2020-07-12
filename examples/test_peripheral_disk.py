from computercraft.subapis.peripheral import CCDrive
from cc import LuaException, import_file, peripheral

_lib = import_file('_lib.py', __file__)


side = 'left'

_lib.step(f'Put empty disk drive on {side} side of computer')

d = peripheral.wrap(side)
assert d is not None

tbl = _lib.get_object_table(f'peripheral.wrap("{side}")')
assert _lib.get_class_table(CCDrive) == tbl

assert d.isDiskPresent() is False
assert d.hasData() is False
assert d.getMountPath() is None
assert d.setDiskLabel('text') is None
assert d.getDiskLabel() is None
assert d.getDiskID() is None
assert d.hasAudio() is False
assert d.getAudioTitle() is False  # False instead None!
assert d.playAudio() is None
assert d.stopAudio() is None
assert d.ejectDisk() is None

_lib.step('Put new CC diskette into disk drive')

assert d.isDiskPresent() is True
assert d.hasData() is True
assert isinstance(d.getMountPath(), str)
assert isinstance(d.getDiskID(), int)

assert d.getDiskLabel() is None
assert d.setDiskLabel('label') is None
assert d.getDiskLabel() == 'label'
assert d.setDiskLabel(None) is None
assert d.getDiskLabel() is None

assert d.hasAudio() is False
assert d.getAudioTitle() is None
assert d.playAudio() is None
assert d.stopAudio() is None

assert d.ejectDisk() is None

_lib.step('Put any audio disk into disk drive')

assert d.isDiskPresent() is True
assert d.hasData() is False
assert d.getMountPath() is None
assert d.getDiskID() is None
assert d.hasAudio() is True

label = d.getAudioTitle()
assert isinstance(label, str)
assert label != 'label'
print(f'Label is {label}')
assert d.getDiskLabel() == label
with _lib.assert_raises(LuaException):
    d.setDiskLabel('label')
with _lib.assert_raises(LuaException):
    d.setDiskLabel(None)
# no effect
assert d.getDiskLabel() == label

assert d.playAudio() is None

_lib.step('Audio must be playing now')

assert d.stopAudio() is None
assert d.ejectDisk() is None

print('Test finished successfully')
