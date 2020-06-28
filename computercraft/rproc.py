from .errors import LuaException


def coro(result):
    assert isinstance(result, list)
    if len(result) < 2:
        result.append(None)
    assert len(result) == 2
    success, result = result
    assert isinstance(success, bool)
    if not success:
        raise LuaException(result)
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


def fact_tuple(*components):
    def proc(result):
        result = any_list(result)
        assert len(components) == result
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


def fact_scheme_dict(components):
    def proc(result):
        result = any_dict(result)
        assert set(result.keys()) == set(components.keys())
        return {key: component(result[key]) for key, component in components.items()}
    return proc


def fact_scheme_dict_kw(**components):
    return fact_scheme_dict(components)


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
