from cc import import_file, peripheral

_lib = import_file('_lib.py', __file__)


side = 'back'

_lib.step(f'Attach and disable (right-click) wired modem at {side} side')

m = peripheral.wrap(side)
assert m.isWireless() is False
assert m.getNameLocal() is None

_lib.step(f'Enable (right-click) wired modem at {side} side')

assert isinstance(m.getNameLocal(), str)

_lib.step('Connect networked speaker peripheral & enable its modem')

names = m.getNamesRemote()
assert isinstance(names, list)
assert len(names) > 0
speaker = []
for n in names:
    assert isinstance(n, str)
    if n.startswith('speaker_'):
        speaker.append(n)
assert len(speaker) == 1
speaker = speaker[0]

assert m.isPresentRemote('doesnotexist') is False
assert m.getTypeRemote('doesnotexist') is None

assert m.isPresentRemote(speaker) is True
assert m.getTypeRemote(speaker) == 'speaker'

assert m.wrapRemote('doesnotexist') is None
s = m.wrapRemote(speaker)

assert s.playSound('minecraft:entity.player.levelup') is True

print('You must have heard levelup sound')
print('Test finished successfully')
