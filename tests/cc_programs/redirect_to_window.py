from cc import colors, term, window


w, h = term.getSize()
left = window.create(
    term.current(),
    1, 1, w // 2, h, True)
right = window.create(
    term.current(),
    w // 2 + 1, 1, w // 2, h, True)
with term.redirect(left):
    term.setBackgroundColor(colors.green)
    term.setTextColor(colors.white)
    term.clear()
    term.setCursorPos(1, h // 2)
    print('Left part')
with term.redirect(right):
    term.setBackgroundColor(colors.red)
    term.setTextColor(colors.yellow)
    term.clear()
    term.setCursorPos(1, h // 2)
    print('Right part')
print('Default terminal restored')

print('Test finished successfully')
