from contextlib import contextmanager
from cc import LuaException, disk


def step(text):
    input(f'{text} [enter]')


@contextmanager
def assert_raises(etype, message=None):
    try:
        yield
    except Exception as e:
        assert isinstance(e, etype), repr(e)
        if message is not None:
            assert e.args == (message, )
    else:
        raise AssertionError(f'Exception of type {etype} was not raised')


s = 'right'

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
assert disk.getAudioTitle(s) is None
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
