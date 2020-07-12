from contextlib import ExitStack

from cc import colors, term, window


w, h = term.getSize()
with ExitStack() as stack:
    left = stack.enter_context(window.create(
        term.get_current_target(),
        1, 1, w // 2, h, True,
    ))
    right = stack.enter_context(window.create(
        term.get_current_target(),
        w // 2 + 1, 1, w // 2, h, True,
    ))
    with term.redirect(left.get_term_target()):
        term.setBackgroundColor(colors.green)
        term.setTextColor(colors.white)
        term.clear()
        term.setCursorPos(1, h // 2)
        print('Left part')
    with term.redirect(right.get_term_target()):
        term.setBackgroundColor(colors.red)
        term.setTextColor(colors.yellow)
        term.clear()
        term.setCursorPos(1, h // 2)
        print('Right part')
    print('Default terminal restored')

print('Test finished successfully')
