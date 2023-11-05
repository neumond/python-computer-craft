from contextlib import contextmanager
from cc import os


@contextmanager
def assert_raises(etype, message=None):
    try:
        yield
    except Exception as e:
        assert isinstance(e, etype), repr(e)
        if message is not None:
            assert e.args == (message, )
    else:
        raise AssertionError(f'Exception of type {etype} was not raised')


@contextmanager
def assert_takes_time(at_least, at_most):
    t = os.epoch('utc') / 1000
    yield
    dt = os.epoch('utc') / 1000 - t
    # print(at_least, '<=', dt, '<=', at_most)
    assert at_least <= dt <= at_most


class AnyInstanceOf:
    def __init__(self, cls):
        self.c = cls

    def __eq__(self, other):
        return isinstance(other, self.c)


def step(text):
    input(f'{text} [enter]')


def term_step(text):
    from cc import colors, term

    for color in colors.iter_colors():
        r, g, b = term.nativePaletteColor(color)
        term.setPaletteColor(color, r, g, b)
    term.setBackgroundColor(colors.black)
    term.setTextColor(colors.white)
    term.clear()
    term.setCursorPos(1, 1)
    term.setCursorBlink(True)
    step(text)


def _computer_peri(place_thing, thing):
    from cc import peripheral

    side = 'left'

    step(
        f'Place {place_thing} on {side} side of computer\n'
        "Don't turn it on!",
    )

    c = peripheral.wrap(side)
    assert c is not None

    assert c.isOn() is False
    assert isinstance(c.getID(), int)
    assert c.getLabel() is None
    assert c.turnOn() is None

    step(f'{thing.capitalize()} must be turned on now')

    assert c.shutdown() is None

    step(f'{thing.capitalize()} must shutdown')

    step(f'Now turn on {thing} manually and enter some commands')

    assert c.reboot() is None

    step(f'{thing.capitalize()} must reboot')

    print('Test finished successfully')
