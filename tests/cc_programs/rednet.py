from cc import LuaException, import_file, os, rednet, parallel

_lib = import_file('_lib.py', __file__)
step, assert_raises = _lib.step, _lib.assert_raises

side = 'back'

step(f'Attach modem to {side} side of computer')

assert rednet.close() is None

assert rednet.isOpen(side) is False
assert rednet.isOpen() is False

with assert_raises(LuaException):
    rednet.close('doesnotexist')

assert rednet.close(side) is None

with assert_raises(LuaException):
    rednet.open('doesnotexist')

assert rednet.open(side) is None
assert rednet.isOpen(side) is True

with assert_raises(LuaException):
    # disallowed hostname
    rednet.host('helloproto', 'localhost')
assert rednet.host('helloproto', 'alpha') is None

cid = os.getComputerID()

assert rednet.lookup('helloproto', 'localhost') == cid
assert rednet.lookup('helloproto') == [cid]
assert rednet.lookup('nonexistent', 'localhost') is None
assert rednet.lookup('nonexistent') == []

assert rednet.unhost('helloproto') is None

assert rednet.send(cid + 100, b'message', 'anyproto') is True
assert rednet.broadcast(b'message', 'anyproto') is None

assert rednet.receive(timeout=1) is None


def _send():
    assert rednet.send(cid, b'message') is True


def _recv():
    assert rednet.receive(timeout=1) == (cid, b'message', None)


parallel.waitForAll(_send, _recv)

assert rednet.close() is None
assert rednet.isOpen(side) is False

print('Test finished successfully')
