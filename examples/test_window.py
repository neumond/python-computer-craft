from cc import colors, term, os, window


with window.create(
    term.get_current_target(),
    15, 5, 5, 5, False,
) as win:
    assert win.getPosition() == (15, 5)
    assert win.getSize() == (5, 5)

    win.setBackgroundColor(colors.red)
    win.clear()
    win.setVisible(True)

    os.sleep(1)

    win.setVisible(False)
    win.setCursorPos(1, 1)
    win.setTextColor(colors.yellow)
    win.write('*********')
    win.setVisible(True)

    os.sleep(1)

    term.clear()

    os.sleep(1)

    win.redraw()
    assert win.getLine(1) == ('*****', b'44444', b'eeeee')

    # draws immediately
    win.reposition(21, 5)
    win.reposition(27, 5)

print('Test finished successfully')
