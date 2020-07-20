from .errors import LuaException


def lua_table_to_list(x, length: int = None):
    if not x:
        return [] if length is None else [None] * length
    assert all(map(lambda k: isinstance(k, int), x.keys()))
    assert min(x.keys()) >= 1
    if length is not None:
        assert max(x.keys()) <= length
    else:
        length = max(x.keys())
    return [x.get(i + 1) for i in range(length)]


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

    def bool_error_exclude(self, exc_msg):
        success = self.take_bool()
        if success:
            return True
        msg = self.take_string()
        if msg == exc_msg:
            return False
        raise LuaException(msg)

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
        return [v.decode('latin1') for v in x]

    def take_list_of_ints(self):
        x = self.take_list()
        assert all(map(lambda v: isinstance(v, int), x))
        return x

    def take_2d_int(self):
        x = self.take_list()
        x = [lua_table_to_list(item) for item in x]
        for row in x:
            for item in row:
                assert isinstance(item, int)
        return x


class TableProc(ResultProc):
    def __init__(self, result, keys):
        self._v = result
        self._keys = keys
        self._i = 0

    def peek(self):
        return self._v.get(self._keys[self._i])


def coro(result):
    assert isinstance(result, list)
    assert len(result) >= 1
    success, *result = result
    assert isinstance(success, bool)
    if not success:
        raise LuaException(result)
    if result == []:
        return None
    if len(result) == 1:
        return result[0]
    return result


def nil(result):
    assert result is None
    return result


def boolean(result):
    assert result is True or result is False
    return result


def integer(result):
    assert isinstance(result, int)
    assert not isinstance(result, bool)
    return result


def number(result):
    assert isinstance(result, (int, float))
    assert not isinstance(result, bool)
    return result


def string(result):
    assert isinstance(result, str)
    return result


def any_dict(result):
    assert isinstance(result, dict)
    return result


def any_list(result):
    if result == {}:
        result = []
    assert isinstance(result, list)
    return result


def fact_tuple(*components, tail_nils=0):
    def proc(result):
        result = any_list(result)
        assert len(components) >= len(result) >= len(components) - tail_nils
        while len(result) < len(components):
            result.append(None)
        assert len(components) == len(result)
        return tuple(comp(value) for comp, value in zip(components, result))
    return proc


def fact_array(component):
    def proc(result):
        result = any_list(result)
        return [component(value) for value in result]
    return proc


def fact_option(component):
    def proc(result):
        if result is None:
            return None
        return component(result)
    return proc


def fact_union(*case_pairs, pelse):
    def proc(result):
        for detector, processor in case_pairs:
            if detector(result):
                return processor(result)
        return pelse(result)
    return proc


def fact_scheme_dict(required, optional):
    required_keys = set(required.keys())
    optional_keys = set(optional.keys())
    assert required_keys & optional_keys == set()
    all_keys = required_keys | optional_keys
    all_fns = required.copy()
    all_fns.update(optional)

    def proc(result):
        result = any_dict(result)
        result_keys = set(result.keys())
        assert result_keys.issubset(all_keys)
        assert required_keys.issubset(result_keys)
        return {key: all_fns[key](value) for key, value in result.items()}
    return proc


def fact_mono_dict(key, value):
    def proc(result):
        result = any_dict(result)
        return {key(k): value(v) for k, v in result.items()}
    return proc


tuple3_number = fact_tuple(number, number, number)
tuple2_integer = fact_tuple(integer, integer)
tuple3_integer = fact_tuple(integer, integer, integer)
tuple3_string = fact_tuple(string, string, string)
array_integer = fact_array(integer)
array_string = fact_array(string)
option_integer = fact_option(integer)
option_string = fact_option(string)
_try_result = fact_tuple(boolean, option_string, tail_nils=1)


def try_result(result):
    success, error_msg = _try_result(result)
    if success:
        assert error_msg is None
        return None
    else:
        raise LuaException(error_msg)


def flat_try_result(result):
    if result is True:
        return None
    return try_result(result)


option_string_bool = fact_option(fact_union(
    (
        lambda v: v is True or v is False,
        boolean,
    ),
    pelse=string,
))
