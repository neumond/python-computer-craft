from cc import import_file, parallel, os, peripheral

_lib = import_file('_lib.py', __file__)
side = 'back'


def do_test():
    m = peripheral.wrap(side)

    remote_channel = 5
    local_channel = 7
    messages = []

    def _send():
        for msg in [
            1,
            b'hi',
            {b'data': 5},
            b'stop',
        ]:
            os.sleep(1)
            m.transmit(remote_channel, local_channel, msg)

    def _recv():
        assert m.isOpen(local_channel) is False
        for msg in m.receive(local_channel):
            assert m.isOpen(local_channel) is True
            assert msg.reply_channel == remote_channel
            assert msg.distance > 0
            messages.append(msg.content)
            if len(messages) == 3:
                break

    assert m.closeAll() is None
    parallel.waitForAll(_recv, _send)

    assert messages == [1, b'hi', {b'data': 5}]
    assert m.isOpen(local_channel) is False
    assert m.closeAll() is None
    assert isinstance(m.isWireless(), bool)


_lib.step(
    f'Attach wired modem to {side} side\n'
    f'Place another computer with wired modem on {side} side\n'
    'Connect modems\n'
    'On another computer start py modem_server.py'
)
do_test()
_lib.step(
    'Disconnect and remove wired modems\n'
    'Attach wireless modems\n'
    'Restart modem_server.py on another computer'
)
do_test()
print('Test finished successfully')
