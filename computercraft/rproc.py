from uuid import UUID

from . import ser
from .errors import LuaException


def lua_table_to_list(x, length: int = None, low_index: int = 1):
    if not x:
        return [] if length is None else [None] * length
    assert all(map(lambda k: isinstance(k, int), x.keys()))
    assert min(x.keys()) >= low_index
    dlen = max(x.keys()) - low_index + 1
    if length is not None:
        assert dlen <= length
    else:
        length = dlen
    return [x.get(i + low_index) for i in range(length)]


class ResultProc:
    def __init__(self, result):
        self._v = result
        self._i = 1

    def forward(self):
        self._i += 1

    def back(self):
        self._i -= 1

    def peek(self):
        return self._v.get(self._i)

    def take(self):
        r = self.peek()
        self.forward()
        return r

    def take_none(self):
        x = self.take()
        assert x is None
        return x

    def take_bool(self):
        x = self.take()
        assert x is True or x is False
        return x

    def take_int(self):
        x = self.take()
        assert isinstance(x, int)
        assert not isinstance(x, bool)
        return x

    def take_rounded_int(self):
        return round(self.take_number())

    def take_number(self):
        x = self.take()
        assert isinstance(x, (int, float))
        assert not isinstance(x, bool)
        return x

    def take_bytes(self):
        x = self.take()
        assert isinstance(x, bytes)
        return x

    def take_string(self):
        return self.take_bytes().decode('latin1')

    def take_unicode(self):
        return self.take_bytes().decode('utf-8')

    def take_uuid(self):
        return UUID(self.take_bytes().decode('ascii'))

    def take_dict(self, keys=None):
        x = self.take()
        assert isinstance(x, dict)
        if keys is None:
            return x
        return TableProc(x, keys)

    def take_list(self, length: int = None):
        return lua_table_to_list(self.take_dict(), length)

    def check_bool_error(self):
        success = self.take_bool()
        if not success:
            raise LuaException(self.take_string())

    def check_nil_error(self):
        if self.peek() is None:
            self.forward()
            raise LuaException(self.take_string())

    def u_check_nil_error(self):
        if self.peek() is None:
            self.forward()
            raise LuaException(self.take_unicode())

    def take_option_int(self):
        if self.peek() is None:
            return self.take_none()
        return self.take_int()

    def take_option_bytes(self):
        if self.peek() is None:
            return self.take_none()
        return self.take_bytes()

    def take_option_string(self):
        if self.peek() is None:
            return self.take_none()
        return self.take_string()

    def take_option_unicode(self):
        if self.peek() is None:
            return self.take_none()
        return self.take_unicode()

    def take_option_string_bool(self):
        p = self.peek()
        if p is None or p is True or p is False:
            self.forward()
            return p
        return self.take_string()

    def take_list_of_strings(self, length: int = None):
        x = self.take_list(length)
        assert all(map(lambda v: isinstance(v, bytes), x))
        return [ser.decode(v) for v in x]

    def take_2d_int(self):
        x = self.take_list()
        x = [lua_table_to_list(item) for item in x]
        for row in x:
            for item in row:
                assert isinstance(item, int)
        return x

    def take_int_or_unicode(self):
        x = self.take()
        if isinstance(x, bytes):
            x = x.decode('utf-8')
        else:
            assert isinstance(x, int)
        assert not isinstance(x, bool)
        return x


class TableProc(ResultProc):
    def __init__(self, result, keys):
        self._v = result
        self._keys = keys
        self._i = 0

    def peek(self):
        return self._v.get(self._keys[self._i])
