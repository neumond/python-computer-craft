from uuid import UUID

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


def _decode_rec(enc, d):
    if isinstance(d, bytes):
        return d.decode(enc)
    if isinstance(d, dict):
        return {
            _decode_rec(enc, k): _decode_rec(enc, v)
            for k, v in d.items()
        }
    if isinstance(d, list):
        return [_decode_rec(enc, v) for v in d]
    return d


class ResultProc:
    def __init__(self, result, enc):
        self._v = result
        self._enc = enc
        self._i = 1

    def forward(self):
        self._i += 1

    def back(self):
        self._i -= 1

    def peek(self):
        return self._v.get(self._i)

    def peek_type(self):
        v = self.peek()
        if v is None:
            return None
        return type(v)

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

    def take_bool_coerce_nil(self):
        x = self.take()
        assert x is True or x is False or x is None
        return bool(x)

    def take_int(self):
        x = self.take()
        assert isinstance(x, int)
        assert not isinstance(x, bool)
        return x

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
        return self.take_bytes().decode(self._enc)

    def take_unicode(self):
        # specific case in CC, reading unicode files
        return self.take_bytes().decode('utf-8')

    def take_uuid(self):
        return UUID(self.take_bytes().decode('ascii'))

    def take_dict(self, decode_bytes=True):
        x = self.take()
        assert isinstance(x, dict)
        if decode_bytes:
            return _decode_rec(self._enc, x)
        return x

    def take_list(self, length: int = None):
        return lua_table_to_list(self.take_dict(), length)

    def take_proc(self):
        x = self.take()
        assert isinstance(x, dict)
        return ResultProc(x, self._enc)

    def check_bool_error(self):
        success = self.take_bool()
        if not success:
            raise LuaException(self.take_string())

    def check_nil_error(self, allow_nil_nil=False):
        if self.peek() is None:
            self.forward()
            if allow_nil_nil and self.peek() is None:
                return
            raise LuaException(self.take_string())

    def take_option_int(self):
        if self.peek() is None:
            return None
        return self.take_int()

    def take_option_bytes(self):
        if self.peek() is None:
            return None
        return self.take_bytes()

    def take_option_string(self):
        if self.peek() is None:
            return None
        return self.take_string()

    def take_option_unicode(self):
        if self.peek() is None:
            return None
        return self.take_unicode()

    def take_option_string_bool(self):
        p = self.peek()
        if p is None or p is True or p is False:
            self.forward()
            return p
        return self.take_string()

    def take_list_of_strings(self, length: int = None):
        x = self.take_list(length)
        assert all(isinstance(v, str) for v in x)
        return x

    def take_2d_int(self):
        x = self.take_list()
        x = [lua_table_to_list(item) for item in x]
        for row in x:
            for item in row:
                assert isinstance(item, int)
        return x
