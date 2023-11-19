from contextlib import contextmanager

from computercraft.errors import LuaException
from oc import filesystem


@contextmanager
def assert_raises(text):
    try:
        yield
    except LuaException as e:
        assert text in e.message, \
            'message mismatch {} != {}'.format(e.message, text)
    else:
        assert False, 'must raise an exception'


val = filesystem.isAutorunEnabled()
filesystem.setAutorunEnabled(False)
filesystem.setAutorunEnabled(True)
filesystem.setAutorunEnabled(val)

assert filesystem.canonical('a/../b/../c') == 'c'
assert filesystem.canonical('/a/../b') == '/b'
assert filesystem.segments('/a/b/c') == ['a', 'b', 'c']
assert filesystem.concat('/a', 'b', '..', 'c') == '/a/c'
assert filesystem.path('/a/b/c/d') == '/a/b/c/'
assert filesystem.name('/a/b/c/d') == 'd'

target = '/testtemp'

if filesystem.isDirectory(target):
    assert filesystem.remove(target) is True

assert filesystem.exists(target) is False
assert filesystem.isDirectory(target) is False

assert filesystem.makeDirectory(target) is True
with assert_raises('already exists'):
    filesystem.makeDirectory(target)

assert filesystem.exists(target) is True
assert filesystem.isDirectory(target) is True

file_a = filesystem.concat(target, 'a.txt')
with filesystem.open(file_a, 'w') as f:
    assert f.write(b'12345') is True
    assert f.seek('set') == 0
    assert f.write(b'67890') is True
    assert f.seek('cur') == 5

with filesystem.open(file_a, 'r') as f:
    assert f.read(10) == b'67890'
    assert f.read(10) is None

file_x = filesystem.concat(target, 'x.txt')
for mdp in ('', 'b'):
    with filesystem.open(file_x, 'w' + mdp) as f:
        assert f.write(bytes(range(256))) is True
    with filesystem.open(file_x, 'r' + mdp) as f:
        assert f.read(300) == bytes(range(256))
    with filesystem.open(file_x, 'w' + mdp) as f:
        assert f.write('привет') is True
    with filesystem.open(file_x, 'r' + mdp) as f:
        assert f.read(300) == 'привет'.encode('utf-8')

file_b = filesystem.concat(target, 'b.txt')
file_c = filesystem.concat(target, 'c.txt')

assert filesystem.copy(file_a + '.notexists', file_b) is False
assert filesystem.copy(file_a, file_b) is True
assert filesystem.copy(file_a, file_b) is True

assert filesystem.rename(file_b + '.notexists', file_c) is False
assert filesystem.rename(file_b, file_c) is True

with assert_raises('no such file'):
    filesystem.remove(file_b + '.notexists')
assert filesystem.remove(file_c) is True

assert filesystem.exists(file_a) is True
assert filesystem.exists(file_b) is False
assert filesystem.exists(file_c) is False
assert filesystem.exists(target) is True

assert filesystem.isDirectory(file_a) is False
assert filesystem.isDirectory(file_b) is False
assert filesystem.isDirectory(target) is True

assert filesystem.isLink(file_a) == (False, None)
assert filesystem.isLink(file_b) == (False, None)
assert filesystem.isLink(target) == (False, None)

assert filesystem.link(file_a, file_b) is True
with assert_raises('already exists'):
    filesystem.link(file_a, file_b)

assert filesystem.isLink(file_b) == (True, file_a)
assert filesystem.exists(file_b) is True
assert filesystem.isDirectory(file_b) is False

assert filesystem.link(target, file_c) is True
assert filesystem.exists(file_c) is True
assert filesystem.isDirectory(file_c) is True

assert filesystem.size(file_a) == 5
assert filesystem.size(file_b) == 5
assert filesystem.size(file_c) == 0
assert filesystem.size(file_a + '.notexists') == 0

lm = filesystem.lastModified(file_a)
assert lm > 0
assert filesystem.lastModified(file_b) == lm
assert filesystem.lastModified(file_c) == 0
assert filesystem.lastModified(file_a + '.notexists') == 0

assert sorted(filesystem.list(target)) == ['a.txt', 'b.txt', 'c.txt', 'x.txt']

root_fs = filesystem.get('/')[0]
mpoint = filesystem.concat(target, 'mpoint')
assert filesystem.list(mpoint) == []
assert filesystem.get(mpoint + '.notexists')[0] == root_fs

for fs, p in filesystem.mounts():
    if fs != root_fs:
        assert filesystem.get(p) == (fs, p)
        assert filesystem.mount(fs, mpoint) is True
        assert filesystem.get(mpoint) == (fs, mpoint)
        assert filesystem.umount(mpoint) is True
        break

assert filesystem.umount(mpoint) is False
assert filesystem.remove(target) is True
