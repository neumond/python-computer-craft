from cc import LuaException, import_file, disk

_lib = import_file('_lib.py', __file__)
step, assert_raises = _lib.step, _lib.assert_raises


s = 'right'

assert _lib.get_class_table(disk) == _lib.get_object_table('disk')

step(f'Make sure there is no disk drive at {s} side')

assert disk.isPresent(s) is False
assert disk.hasData(s) is False
assert disk.getMountPath(s) is None
assert disk.setLabel(s, 'text') is None
assert disk.getLabel(s) is None
assert disk.getID(s) is None
assert disk.hasAudio(s) is False
assert disk.getAudioTitle(s) is None
assert disk.playAudio(s) is None
assert disk.stopAudio(s) is None
assert disk.eject(s) is None

step(f'Place empty disk drive at {s} side')

assert disk.isPresent(s) is False
assert disk.hasData(s) is False
assert disk.getMountPath(s) is None
assert disk.setLabel(s, 'text') is None
assert disk.getLabel(s) is None
assert disk.getID(s) is None
assert disk.hasAudio(s) is False
assert disk.getAudioTitle(s) is False  # False instead None!
assert disk.playAudio(s) is None
assert disk.stopAudio(s) is None
assert disk.eject(s) is None

step('Put new CC diskette into disk drive')

assert disk.isPresent(s) is True
assert disk.hasData(s) is True
assert isinstance(disk.getMountPath(s), str)
assert isinstance(disk.getID(s), int)

assert disk.getLabel(s) is None
assert disk.setLabel(s, 'label') is None
assert disk.getLabel(s) == 'label'
assert disk.setLabel(s, None) is None
assert disk.getLabel(s) is None

assert disk.hasAudio(s) is False
assert disk.getAudioTitle(s) is None
assert disk.playAudio(s) is None
assert disk.stopAudio(s) is None

assert disk.eject(s) is None

step('Put any audio disk into disk drive')

assert disk.isPresent(s) is True
assert disk.hasData(s) is False
assert disk.getMountPath(s) is None
assert disk.getID(s) is None
assert disk.hasAudio(s) is True

label = disk.getAudioTitle(s)
assert isinstance(label, str)
assert label != 'label'
print(f'Label is {label}')
assert disk.getLabel(s) == label
with assert_raises(LuaException):
    assert disk.setLabel(s, 'label') is None
with assert_raises(LuaException):
    assert disk.setLabel(s, None) is None
# no effect
assert disk.getLabel(s) == label

assert disk.playAudio(s) is None

step('Audio must be playing now')

assert disk.stopAudio(s) is None
assert disk.eject(s) is None

print('Test finished successfully')
