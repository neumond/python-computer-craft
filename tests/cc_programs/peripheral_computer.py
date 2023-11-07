from cc import import_file, peripheral

_lib = import_file('_lib.py', __file__)


def computer_peri(place_thing, thing, finish):
    side = 'left'

    _lib.step(
        f'Place {place_thing} on {side} side of computer\n'
        "Don't turn it on!",
    )

    c = peripheral.wrap(side)
    assert c is not None

    assert c.isOn() is False
    assert isinstance(c.getID(), int)
    assert c.getLabel() is None
    assert c.turnOn() is None

    _lib.step(f'{thing.capitalize()} must be turned on now')

    assert c.shutdown() is None

    _lib.step(f'{thing.capitalize()} must shutdown')

    _lib.step(f'Now turn on {thing} manually and enter some commands')

    assert c.reboot() is None

    _lib.step(f'{thing.capitalize()} must reboot')

    print(f'Test {finish} finished successfully')


computer_peri('another computer', 'computer', '1/2')
computer_peri('turtle', 'turtle', '2/2')
