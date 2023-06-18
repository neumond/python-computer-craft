from oc import sides, colors, keyboard


def check_iterable(m, mlen):
    n = 0
    for i, v in m:
        assert m[i] == v
        assert getattr(m, v) == i
        n += 1
    assert len(m) == n == mlen > 0


assert sides.left == 5
assert sides.forward == 3
assert sides[2] == 'back'
check_iterable(sides, 6)

assert colors.yellow == 4
assert colors[14] == 'red'
check_iterable(colors, 16)

assert keyboard.keys.a == 0x1E
assert keyboard.keys[0x40] == 'f6'
check_iterable(keyboard.keys, len(keyboard.keys))

assert keyboard.isAltDown() is False
assert keyboard.isControlDown() is False
assert keyboard.isShiftDown() is False
assert keyboard.isKeyDown('a') is False
assert keyboard.isKeyDown(keyboard.keys.b) is False

assert keyboard.isControl(0) is True
assert keyboard.isControl(keyboard.keys.c) is False
