from computercraft.subapis.peripheral import CCMonitor
from computercraft.subapis.mixins import TermMixin
from cc import import_file, colors, os, peripheral

_lib = import_file('_lib.py', __file__)


side = 'left'

_lib.step(
    'Use advanced computer and monitor for colors\n'
    f'Place single block monitor on {side} side of computer',
)

m = peripheral.wrap(side)
assert m is not None


tbl = _lib.get_object_table(f'peripheral.wrap("{side}")')

# remove British method names to make API lighter
del tbl['function']['getBackgroundColour']
del tbl['function']['getPaletteColour']
del tbl['function']['getTextColour']
del tbl['function']['isColour']
del tbl['function']['setBackgroundColour']
del tbl['function']['setPaletteColour']
del tbl['function']['setTextColour']
# NOTE: peripheral doesn't have nativePaletteColor method

assert _lib.get_multiclass_table(TermMixin, CCMonitor) == tbl


assert m.getSize() == (7, 5)
assert m.isColor() is True
assert m.setTextColor(colors.white) is None
assert m.setBackgroundColor(colors.black) is None
assert m.clear() is None
assert m.setCursorPos(1, 1) is None
assert m.getCursorPos() == (1, 1)
assert m.write('Alpha') is None
assert m.getCursorPos() == (6, 1)
assert m.setCursorBlink(False) is None
assert m.getCursorBlink() is False
assert m.setCursorBlink(True) is None
assert m.getCursorBlink() is True

_lib.step('You must have seen word Alpha with blinking cursor')

assert m.clear() is None
assert m.setCursorBlink(False) is None
for offs, (tc, bc) in enumerate((
    (colors.lime, colors.green),
    (colors.yellow, colors.brown),
    (colors.red, colors.orange),
), start=1):
    assert m.setTextColor(tc) is None
    assert m.getTextColor() == tc
    assert m.setBackgroundColor(bc) is None
    assert m.getBackgroundColor() == bc
    assert m.setCursorPos(offs, offs) is None
    assert m.getCursorPos() == (offs, offs)
    assert m.write('text') is None
assert m.setBackgroundColor(colors.black) is None
os.sleep(1)
for i in range(2):
    assert m.scroll(-1) is None
    os.sleep(0.5)
for i in range(2):
    assert m.scroll(1) is None
    os.sleep(0.5)

_lib.step('You must have seen three texts with different colors scrolling')

assert m.setTextColor(colors.white) is None
assert m.setBackgroundColor(colors.black) is None
assert m.clear() is None
for i in range(1, 5):
    assert m.setCursorPos(1, i) is None
    assert m.write((str(i) + '  ') * 4) is None
os.sleep(2)
for i in range(2, 5, 2):
    assert m.setCursorPos(1, i) is None
    assert m.clearLine() is None

_lib.step('You must have seen some lines disappearing')

assert m.setBackgroundColor(colors.black) is None
assert m.clear() is None
assert m.setCursorPos(1, 1) is None
assert m.blit(
    'rainbow',
    'e14d3ba',
    'fffffff',
) is None
assert m.setCursorPos(1, 2) is None
assert m.blit(
    'rainbow',
    '0000000',
    'e14d3ba',
) is None

_lib.step('You must have seen per-letter colored text')

assert m.setBackgroundColor(colors.black) is None
assert m.setTextColor(colors.white) is None
assert m.getTextScale() == 1
assert m.setTextScale(5) is None
assert m.getTextScale() == 5
assert m.setCursorPos(1, 1) is None
assert m.clear() is None
assert m.getSize() == (1, 1)
assert m.write('AAA') is None

_lib.step('You must have seen single large letter A')

assert m.setTextScale(1) is None
assert m.setBackgroundColor(colors.white) is None
assert m.clear() is None
for i, color in enumerate(colors.iter_colors()):
    m.setPaletteColor(color, i / 15, 0, 0)
assert m.setCursorPos(1, 1) is None
assert m.blit(
    ' redtex',
    '0123456',
    '0000000',
) is None
assert m.setCursorPos(1, 2) is None
assert m.blit(
    'tappear',
    '789abcd',
    '0000000',
) is None
assert m.setCursorPos(1, 3) is None
assert m.blit(
    's!',
    'ef',
    '00',
) is None

_lib.step('You must have seen different shades of red made using palettes')

print('Remove monitor')
print('Test finished successfully')
