from contextlib import contextmanager
from time import monotonic
from types import FunctionType

from cc import eval_lua


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
    t = monotonic()
    yield
    dt = monotonic() - t
    # print(at_least, '<=', dt, '<=', at_most)
    assert at_least <= dt <= at_most


class AnyInstanceOf:
    def __init__(self, cls):
        self.c = cls

    def __eq__(self, other):
        return isinstance(other, self.c)


def step(text):
    input(f'{text} [enter]')


def get_object_table(objname):
    rp = eval_lua(f"""
local r = {{}}
for k in pairs({objname}) do
    local t = type({objname}[k])
    if r[t] == nil then r[t] = {{}} end
    if t == 'number' or t == 'boolean' or t == 'string' then
        r[t][k] = {objname}[k]
    else
        r[t][k] = true
    end
end
return r""", immediate=True)
    d = rp.take_dict()
    return {
        k1.decode('latin1'): {
            k2.decode('latin1'): v for k2, v in t.items()
        } for k1, t in d.items()
    }


def get_class_table(cls):
    items = {
        k: v for k, v in vars(cls).items()
        if not k.startswith('_')
    }
    nums = {
        k: v for k, v in items.items()
        if isinstance(v, (int, float))
    }
    methods = {
        k: True for k, v in items.items()
        if isinstance(v, FunctionType)
    }
    r = {}
    if nums:
        r['number'] = nums
    if methods:
        r['function'] = methods
    return r


def get_multiclass_table(*cls):
    result = {}
    for c in cls:
        for k, v in get_class_table(c).items():
            result.setdefault(k, {}).update(v)
    return result


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

    from computercraft.cc.peripheral import ComputerMixin
    tbl = get_object_table(f'peripheral.wrap("{side}")')
    assert get_class_table(ComputerMixin) == tbl

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
