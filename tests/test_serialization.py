from math import inf, nan, isnan

import pytest

from computercraft.ser import serialize, deserialize


@pytest.mark.parametrize('v', [
    None,
    True,
    False,
    0,
    -1,
    1,
    1e6,
    1.5,
    2.4e-9,
    inf,
    -inf,
    b'',
    b'string',
    b'\n\r\0',
    b'\0',
    b'2',
    {},
    {2: 4},
    {b'a': 1, b'b': None, b'c': {}, b'd': {b'x': 8}},
])
def test_roundtrip(v):
    assert v == deserialize(serialize(v))


def test_nan():
    assert isnan(deserialize(serialize(nan)))


@pytest.mark.parametrize('a,b', [
    ([1], {1: 1}),
    ([1, 2, 3], {1: 1, 2: 2, 3: 3}),
    ([b'abc'], {1: b'abc'}),
    ([b'a', b'b', b'c'], {1: b'a', 2: b'b', 3: b'c'}),
])
def test_oneway(a, b):
    assert b == deserialize(serialize(a))
