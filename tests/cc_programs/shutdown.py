from cc import os


if args[-1:] == [b'reboot']:
    assert os.reboot() is None
else:
    assert os.shutdown() is None
print('Test finished successfully')
