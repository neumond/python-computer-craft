import random

from cc import import_file, os, peripheral

_lib = import_file('_lib.py', __file__)

random.seed(598392)
side = 'left'

_lib.step(f'Attach speaker at {side} side of computer')

m = peripheral.wrap(side)

for _ in range(48):
    assert m.playNote(
        random.choice([
            'bass', 'basedrum', 'bell', 'chime', 'flute', 'guitar', 'hat',
            'snare', 'xylophone', 'iron_xylophone', 'pling', 'banjo',
            'bit', 'didgeridoo', 'cow_bell',
        ]),
        3,
        random.randint(0, 24)
    ) is True
    os.sleep(0.2)

assert m.playSound('minecraft:entity.player.levelup') is True

print('You must have heard notes and sounds')
print('Test finished successfully')
