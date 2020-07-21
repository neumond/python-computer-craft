from cc import LuaException, import_file, fs

_lib = import_file('_lib.py', __file__)
assert_raises, AnyInstanceOf = _lib.assert_raises, _lib.AnyInstanceOf


assert _lib.get_class_table(fs) == _lib.get_object_table('fs')

for name in ('tdir', 'tfile'):
    if fs.exists(name):
        fs.delete(name)

assert fs.makeDir('tdir') is None
with fs.open('tfile', 'w') as f:
    f.writeLine('textline')

dlist = set(fs.list('.'))

assert {'tdir', 'tfile', 'rom'}.issubset(dlist)
assert fs.list('tdir') == []

capacity = fs.getCapacity('.')
free = fs.getFreeSpace('.')
assert isinstance(capacity, int)
assert isinstance(free, int)
assert free < capacity
assert free > 0
assert capacity > 0

assert fs.exists('tdir') is True
assert fs.exists('tfile') is True
assert fs.exists('doesnotexist') is False

assert fs.isDir('tdir') is True
assert fs.isDir('tfile') is False
assert fs.isDir('doesnotexist') is False

assert fs.isReadOnly('rom') is True
assert fs.isReadOnly('tdir') is False
assert fs.isReadOnly('tfile') is False
assert fs.isReadOnly('doesnotexist') is False

assert fs.getDrive('rom') == 'rom'
assert fs.getDrive('tdir') == 'hdd'
assert fs.getDrive('tfile') == 'hdd'
assert fs.getDrive('doesnotexist') is None

assert fs.isDriveRoot('/') is True
assert fs.isDriveRoot('rom') is True
assert fs.isDriveRoot('tdir') is False
assert fs.isDriveRoot('tfile') is False
assert fs.isDriveRoot('doesnotexist') is True  # wtf?

assert fs.getName('a/b/c/d') == 'd'
assert fs.getName('a/b/c/') == 'c'
assert fs.getName('/a/b/c/d') == 'd'
assert fs.getName('///a/b/c/d') == 'd'
assert fs.getName('') == 'root'  # wtf?
assert fs.getName('/') == 'root'
assert fs.getName('///') == 'root'
assert fs.getName('.') == 'root'
assert fs.getName('..') == '..'
assert fs.getName('../../..') == '..'

assert fs.getDir('a/b/c/d') == 'a/b/c'
assert fs.getDir('a/b/c/') == 'a/b'
assert fs.getDir('/a/b/c/d') == 'a/b/c'
assert fs.getDir('///a/b/c/d') == 'a/b/c'
assert fs.getDir('') == '..'
assert fs.getDir('/') == '..'
assert fs.getDir('///') == '..'
assert fs.getDir('.') == '..'
assert fs.getDir('..') == ''
assert fs.getDir('../../..') == '../..'

assert fs.combine('a', 'b') == 'a/b'
assert fs.combine('a/', 'b') == 'a/b'
assert fs.combine('a//', 'b') == 'a/b'
assert fs.combine('a/', '/b') == 'a/b'
assert fs.combine('a/b/c', '..') == 'a/b'
assert fs.combine('a/b/c', '../..') == 'a'
assert fs.combine('a/b/c', '../../..') == ''
assert fs.combine('a/b/c', '../../../..') == '..'
assert fs.combine('a/b/c', '../../../../..') == '../..'
assert fs.combine('/a/b/c', '../../../../..') == '../..'
assert fs.combine('a/b/c', '////') == 'a/b/c'
assert fs.combine('a/b/c', '.') == 'a/b/c'
assert fs.combine('a/b/c', './.') == 'a/b/c'
assert fs.combine('a/b/c', './../.') == 'a/b'

assert fs.getSize('tfile') == 9
assert fs.getSize('tdir') == 0
with assert_raises(LuaException):
    fs.getSize('doesnotexist')

assert fs.move('tfile', 'tdir/apple') is None
assert fs.list('tdir') == ['apple']
assert fs.copy('tdir/apple', 'tdir/banana') is None
assert fs.list('tdir/') == ['apple', 'banana']
assert fs.copy('tdir/apple', 'tdir/cherry') is None

assert fs.getSize('tdir') == 0

dlist = set(fs.find('*'))
assert 'tdir' in dlist
assert 'rom' in dlist
assert 'tfile' not in dlist
assert 'tdir/apple' not in dlist

dlist = set(fs.find('tdir/*'))
assert dlist == {'tdir/apple', 'tdir/banana', 'tdir/cherry'}

dlist = set(fs.find('tdir/*a*'))
assert dlist == {'tdir/apple', 'tdir/banana'}

dlist = set(fs.find('**'))
assert 'tdir' in dlist
assert 'tdir/apple' not in dlist  # not recursive

dlist = set(fs.list(''))
assert 'tfile' not in dlist
assert 'tdir' in dlist
assert 'rom' in dlist

dlist = set(fs.list('tdir'))
assert dlist == {'apple', 'banana', 'cherry'}

assert fs.attributes('tdir/banana') == {
    'created': AnyInstanceOf(int),
    'modification': AnyInstanceOf(int),
    'isDir': False,
    'size': 9,
}
assert fs.attributes('tdir') == {
    'created': AnyInstanceOf(int),
    'modification': AnyInstanceOf(int),
    'isDir': True,
    'size': 0,
}
with assert_raises(LuaException):
    fs.attributes('doesnotexist')

assert fs.complete('ba', 'tdir') == ['nana']
assert fs.complete('ap', 'tdir') == ['ple']
assert fs.complete('c', 'tdir') == ['herry']
assert fs.complete('td', '') == ['ir/', 'ir']
assert fs.complete('td', '', includeDirs=True) == ['ir/', 'ir']
assert fs.complete('td', '', includeDirs=False) == ['ir/']  # wtf?
assert fs.complete('ap', 'tdir', includeFiles=True) == ['ple']
assert fs.complete('ap', 'tdir', includeFiles=False) == []

assert fs.getSize('tdir/banana') == 9
with fs.open('tdir/banana', 'r') as f:
    assert f.read(4) == 'text'
    assert f.readLine() == 'line'
    assert f.read(1) is None
    assert f.readLine() is None
    assert f.readAll() is None
    assert f.readAll() is None
assert fs.getSize('tdir/banana') == 9
with fs.open('tdir/banana', 'a') as f:
    assert f.write('x') is None
assert fs.getSize('tdir/banana') == 10
with fs.open('tdir/banana', 'w') as f:
    pass
assert fs.getSize('tdir/banana') == 0  # truncate
with fs.open('tdir/banana', 'w') as f:
    assert f.write('Bro') is None
    assert f.writeLine('wn fox jumps') is None
    # assert fs.getSize('tdir/banana') == 0  # changes are not on a disk
    assert f.flush() is None
    assert fs.getSize('tdir/banana') == len('Brown fox jumps\n')
    assert f.write('ov') is None
    assert f.write('er ') is None
    assert f.write('a lazy') is None
    assert f.writeLine(' дог.') is None  # supports unicode!
assert fs.getSize('tdir/banana') > 9
with fs.open('tdir/banana', 'r') as f:
    assert f.readAll() == 'Brown fox jumps\nover a lazy дог.\n'
with assert_raises(LuaException):
    with fs.open('tdir/banana', 'rw') as f:
        pass

assert fs.exists('tdir/banana') is True

with fs.open('tdir/binfile', 'wb') as f:
    assert f.write(b'a' * 9) is None
    assert f.seek() == 9
    assert f.seek('set', 0) == 0
    assert f.write(b'b' * 3) is None
    assert f.seek('cur', -1) == 2
    assert f.write(b'c' * 3) is None
    assert f.seek('end') == 9
    assert f.write(b'd' * 3) is None
    with assert_raises(LuaException):
        f.seek('set', -10)

with fs.open('tdir/binfile', 'rb') as f:
    assert f.readAll() == b'bbcccaaaaddd'

with fs.open('tdir/binfile', 'r') as f:
    assert [line for line in f] == ['bbcccaaaaddd']

assert fs.delete('tdir') is None
assert fs.delete('tfile') is None
assert fs.delete('doesnotexist') is None

assert fs.exists('tdir/banana') is False

print('Test finished successfully')
