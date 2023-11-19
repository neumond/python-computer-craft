import uuid
from contextlib import contextmanager

from computercraft.errors import LuaException
from oc import component


@contextmanager
def assert_raises(text):
    try:
        yield
    except LuaException as e:
        assert text in e.message, \
            'message mismatch {} != {}'.format(e.message, text)
    else:
        assert False, 'must raise an exception'


assert component.isAvailable('gpu') is True
assert component.isAvailable('nonexistent') is False
cs = component.list()

inv_addr = uuid.UUID(int=0)
assert inv_addr not in cs

for addr, ctype in cs.items():
    assert component.type(addr) == ctype
    slot = component.slot(addr)
    assert isinstance(slot, int)
    print('{} {}'.format(slot, ctype))

with assert_raises('no such component'):
    component.type(inv_addr)
with assert_raises('no such component'):
    component.slot(inv_addr)

assert isinstance(component.getPrimaryAddress('gpu'), uuid.UUID)
with assert_raises("no primary 'nonexistent' available"):
    component.getPrimaryAddress('nonexistent')

gpu = component.getPrimary('gpu')
assert 1 <= gpu.getDepth() <= 256
print(gpu)
