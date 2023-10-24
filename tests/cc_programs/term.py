from cc import colors, term, os


def step(text):
    input(f'{text} [enter]')


def term_step(text):
    for color in colors.iter_colors():
        r, g, b = term.nativePaletteColor(color)
        term.setPaletteColor(color, r, g, b)
    term.setBackgroundColor(colors.black)
    term.setTextColor(colors.white)
    term.clear()
    term.setCursorPos(1, 1)
    term.setCursorBlink(True)
    step(text)


step(
    'Detach all monitors\n'
    'Use advanced computer for colors\n'
    'Screen will be cleared'
)

assert term.getSize() == (51, 19)
assert term.isColor() is True
assert term.clear() is None
assert term.setCursorPos(1, 1) is None
assert term.getCursorPos() == (1, 1)
assert term.write('Alpha') is None
assert term.getCursorPos() == (6, 1)
assert term.setCursorBlink(False) is None
assert term.getCursorBlink() is False
assert term.setCursorBlink(True) is None
assert term.getCursorBlink() is True
os.sleep(2)

term_step('You must have seen word Alpha with blinking cursor')

assert term.clear() is None
for offs, (tc, bc) in enumerate((
    (colors.lime, colors.green),
    (colors.yellow, colors.brown),
    (colors.red, colors.orange),
), start=1):
    assert term.setTextColor(tc) is None
    assert term.getTextColor() == tc
    assert term.setBackgroundColor(bc) is None
    assert term.getBackgroundColor() == bc
    assert term.setCursorPos(offs * 2, offs) is None
    assert term.getCursorPos() == (offs * 2, offs)
    assert term.write('text with colors') is None
assert term.setBackgroundColor(colors.black) is None
os.sleep(1)
for i in range(3):
    assert term.scroll(-2) is None
    os.sleep(0.5)
for i in range(6):
    assert term.scroll(1) is None
    os.sleep(0.25)

term_step('You must have seen three texts with different colors scrolling')

assert term.clear() is None
for i in range(1, 10):
    assert term.setCursorPos(1, i) is None
    assert term.write((str(i) + '  ') * 10) is None
os.sleep(2)
for i in range(2, 10, 2):
    assert term.setCursorPos(1, i) is None
    assert term.clearLine() is None
os.sleep(2)

term_step('You must have seen some lines disappearing')

assert term.clear() is None
assert term.setCursorPos(1, 1) is None
assert term.blit(
    'rainbowrainbow',
    b'e14d3ba0000000',
    b'fffffffe14d3ba',
) is None
os.sleep(3)

term_step('You must have seen per-letter colored text')

assert term.setBackgroundColor(colors.white) is None
assert term.clear() is None
assert term.setCursorPos(1, 1) is None
for i, color in enumerate(colors.iter_colors()):
    term.setPaletteColor(color, i / 15, 0, 0)
assert term.blit(
    ' redtextappears!',
    b'0123456789abcdef',
    b'0000000000000000',
) is None
os.sleep(3)

term_step('You must have seen different shades of red made using palettes')

print('Test finished successfully')
