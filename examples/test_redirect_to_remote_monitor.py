from cc import import_file, colors, term, peripheral

_lib = import_file('_lib.py', __file__)


side = 'back'
_lib.step(f'Attach wired modem to {side} side of computer')

mod = peripheral.wrap(side)

_lib.step('Connect remote monitor using wires, activate its modem')

for name in mod.getNamesRemote():
    if mod.getTypeRemote(name) == 'monitor':
        break
else:
    assert False

with term.redirect(peripheral.get_term_target(name)):
    term.setBackgroundColor(colors.blue)
    term.setTextColor(colors.white)
    term.clear()
    term.setCursorPos(1, 1)
    print('Redirected to monitor')

print('Test finished successfully')
