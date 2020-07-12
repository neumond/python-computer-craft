from cc import import_file, colors, term, peripheral

_lib = import_file('_lib.py', __file__)


side = 'left'
_lib.step(f'Attach 3x3 color monitor to {side} side of computer')

with term.redirect(peripheral.get_term_target(side)):
    term.setBackgroundColor(colors.green)
    term.setTextColor(colors.white)
    term.clear()
    term.setCursorPos(1, 1)
    print('Redirected to monitor')

print('Test finished successfully')
