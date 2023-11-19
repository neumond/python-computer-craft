from cc import colors, term, peripheral


side = 'back'
input(f'Attach wired modem to {side} side of computer [enter]')

mod = peripheral.wrap(side)

input('Connect remote monitor using wires, activate its modem [enter]')

for name in mod.getNamesRemote():
    if mod.getTypeRemote(name) == 'monitor':
        break
else:
    assert False

with term.redirect(peripheral.wrap(name)):
    term.setBackgroundColor(colors.blue)
    term.setTextColor(colors.white)
    term.clear()
    term.setCursorPos(1, 1)
    print('Redirected to monitor')

print('Test finished successfully')
