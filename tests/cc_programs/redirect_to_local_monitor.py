from cc import colors, term, peripheral


side = 'left'
input(f'Attach 3x3 color monitor to {side} side of computer [enter]')

with term.redirect(peripheral.wrap(side)):
    term.setBackgroundColor(colors.green)
    term.setTextColor(colors.white)
    term.clear()
    term.setCursorPos(1, 1)
    print('Redirected to monitor')

print('Test finished successfully')
