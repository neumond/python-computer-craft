from oc import term


assert term.isAvailable() is True
term.clear()
term.setCursor(1, 1)
assert term.getCursor() == (1, 1)

blink = term.getCursorBlink()
term.setCursorBlink(False)
term.setCursorBlink(True)
term.setCursorBlink(blink)
assert term.getCursorBlink() == blink
print('Screen', term.screen())
print('Keyboard', term.keyboard())

width, height, xoff, yoff, relx, rely = term.getViewport()
print('Width={} Height={}'.format(width, height))
print('Offset X={} Y={}'.format(xoff, yoff))
print('Relative X={} Y={}'.format(relx, rely))

term.write('Write text no wrap')
term.clearLine()
term.write('Write text with wrap. ' * 7 + '\n', True)

term.write('Input "qwerty" twice:\n')
assert term.read(dobreak=False) == 'qwerty\n'
term.clearLine()
assert term.read(pwchar='*') == 'qwerty\n'
term.write('\nInput "привет":\n')
assert term.read() == 'привет\n'
term.write('Press ctrl+D in this input:\n')
assert term.read() is None
