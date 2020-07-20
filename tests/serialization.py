from math import inf, nan, isnan

from computercraft.ser import serialize, deserialize


roundtrip_vals = [
    None,
    True,
    False,
    0,
    -1,
    1,
    1e6,
    1.5,
    2.4e-9,
    # nan,
    inf,
    -inf,
    '',
    'string',
    '\n\r\0',
    '\0',
    '2',
    {},
    {2: 4},
    {'a': 1, 'b': None, 'c': {}, 'd': {'x': 8}},
    [1, 2, 3],
    [1],
    ['abc'],
]


for v in roundtrip_vals:
    print(serialize(v))
    assert v == deserialize(serialize(v))


print(serialize(nan))
assert isnan(deserialize(serialize(nan)))


oneway_vals = [
    ({1: 'a', 2: 'b', 3: 'c'}, ['a', 'b', 'c']),
]


for a, b in oneway_vals:
    print(serialize(a))
    assert b == deserialize(serialize(a))
