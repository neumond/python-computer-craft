from .errors import LuaException


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
