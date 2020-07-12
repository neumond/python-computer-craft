from cc import import_file, os, parallel

_lib = import_file('_lib.py', __file__)
assert_takes_time, assert_raises = _lib.assert_takes_time, _lib.assert_raises


tags = set()


def partial(tag, fn, *args):
    def wrap():
        tags.add(tag)
        return fn(*args)
    return wrap


all_parallels = [
    ('waitForAll', parallel.waitForAll),
    ('waitForAny', parallel.waitForAny),
]


for name, fn in all_parallels:
    tags.clear()
    with assert_takes_time(1.5, 3):
        # Since os.sleep is mostly waiting for events, it doesn't block execution of parallel threads
        # and this snippet takes approximately 2 seconds to complete.
        fn(
            partial('a', os.sleep, 2),
            partial('b', os.sleep, 2),
            partial('c', os.sleep, 2),
        )
    assert tags == {'a', 'b', 'c'}
    print(name, 'OK')


for name, fn in all_parallels:
    tags.clear()
    tts = (0, 1) if name == 'waitForAny' else (1.5, 3)
    with assert_takes_time(*tts):
        fn(
            partial('fast', os.version),
            partial('s1', os.sleep, 2),
            partial('s2', os.sleep, 2),
        )
    assert tags == {'fast', 's1', 's2'}
    print(name, 'fast OK')


def breaks_fast(etype):
    os.sleep(0.5)
    raise etype


def breaks_slow(etype):
    os.sleep(3)
    raise etype


tags.clear()
with assert_takes_time(0, 1):
    parallel.waitForAny(
        partial('fast', os.version),
        partial('bomb', breaks_slow, IndexError),
    )
assert tags == {'fast', 'bomb'}
print('waitForAny fast success OK')


tags.clear()
with assert_takes_time(2.5, 3.8):
    with assert_raises(IndexError):
        parallel.waitForAll(
            partial('fast', os.version),
            partial('bomb', breaks_slow, IndexError),
        )
assert tags == {'fast', 'bomb'}
print('waitForAll waits for bomb OK')


for name, fn in all_parallels:
    tags.clear()
    with assert_takes_time(0.4, 1.2):
        with assert_raises(ValueError):
            fn(
                partial('v', breaks_fast, ValueError),
                partial('s', os.sleep, 2),
                partial('i', breaks_slow, IndexError),
            )
    os.sleep(4)
    assert tags == {'v', 's', 'i'}
    print(name + ' handles error OK')


for name, fn in all_parallels:
    tags.clear()
    with assert_takes_time(1.5, 3):
        fn(
            partial('1_s', os.sleep, 2),
            partial(
                '1_p',
                fn,
                partial('2_s', os.sleep, 2),
                partial(
                    '2_p',
                    fn,
                    partial('3_s', os.sleep, 2),
                ),
            ),
        )
    assert tags == {'1_s', '1_p', '2_s', '2_p', '3_s'}
    print('Nested', name, 'OK')


def nested_err():
    parallel.waitForAll(
        partial('n_v', breaks_fast, ValueError),
        partial('n_s', os.sleep, 2),
        partial('n_i', breaks_slow, IndexError),
    )


tags.clear()
with assert_takes_time(0.4, 1.2):
    with assert_raises(ValueError):
        parallel.waitForAll(
            nested_err,
            partial('s', os.sleep, 2),
            partial('i', breaks_slow, IndexError),
        )
assert tags == {'s', 'i', 'n_v', 'n_s', 'n_i'}
print('Nested errors OK')


print('Test finished successfully')
