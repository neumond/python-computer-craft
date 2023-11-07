from cc import LuaException, import_file, peripheral

_lib = import_file('_lib.py', __file__)
assert_raises = _lib.assert_raises

side = 'left'

_lib.step(f'Attach empty printer at {side} side of computer')

m = peripheral.wrap(side)

assert m.getPaperLevel() == 0
assert m.getInkLevel() == 0

# no paper
assert m.newPage() is False
# page not started
with assert_raises(LuaException):
    m.endPage()
with assert_raises(LuaException):
    m.write('test')
with assert_raises(LuaException):
    m.setCursorPos(2, 2)
with assert_raises(LuaException):
    m.getCursorPos()
with assert_raises(LuaException):
    m.getPageSize()
with assert_raises(LuaException):
    m.setPageTitle('title')

_lib.step('Put paper into printer')
paper_level = m.getPaperLevel()
assert paper_level > 0
# no ink
assert m.newPage() is False

_lib.step('Put ink into printer')
ink_level = m.getInkLevel()
assert ink_level > 0

assert m.newPage() is True
assert m.getPaperLevel() < paper_level
assert m.getInkLevel() < ink_level

assert m.setCursorPos(2, 2) is None
assert m.getCursorPos() == (2, 2)
assert m.setCursorPos(1, 1) is None
assert m.getCursorPos() == (1, 1)
assert m.setPageTitle('Green bottles') is None
assert m.getPageSize() == (25, 21)


def row(n=1):
    _, r = m.getCursorPos()
    m.setCursorPos(1, r + n)


def split_text(text, max_width=25):
    for i in range(0, len(text), max_width):
        yield text[i:i + max_width]


def split_by_words(text, max_width=25):
    stack = []
    stack_len = 0
    for word in text.split(' '):
        assert len(word) <= max_width
        with_word = len(word) if stack_len == 0 else stack_len + 1 + len(word)
        if with_word > max_width:
            yield ' '.join(stack)
            stack.clear()
            stack_len = 0
        else:
            stack.append(word)
            stack_len = with_word
    if stack:
        yield ' '.join(stack)


def multiline_write(text):
    _, r = m.getCursorPos()
    for pt in split_by_words(text):
        assert m.setCursorPos(1, r) is None
        assert m.write(pt) is None
        r += 1
    assert m.setCursorPos(1, r) is None


assert m.write('Green bottles'.center(25)) is None
row(2)

x = 2
while x > 0:
    multiline_write(f'{x} green bottles hanging on the wall')
    multiline_write(f'{x} green bottles hanging on the wall')
    multiline_write('if one green bottle accidently falls')
    x -= 1
    multiline_write(f'there will be {x} hanging on the wall')
    row()

assert m.endPage() is True

print('Test finished successfully')
