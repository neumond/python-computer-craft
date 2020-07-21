from cc import LuaException, import_file, fs, settings

_lib = import_file('_lib.py', __file__)
step, assert_raises = _lib.step, _lib.assert_raises


assert _lib.get_class_table(settings) == _lib.get_object_table('settings')

step('Settings will be cleared')

assert settings.clear() is None
# names are not empty, there are system settings
assert isinstance(settings.getNames(), list)

assert settings.define('test.a') is None
assert settings.define('test.b', description='b') is None
assert settings.define('test.c', type='string') is None
assert settings.define('test.d', default=42) is None

assert settings.getDetails('test.a') == {
    'changed': False,
}
assert settings.getDetails('test.b') == {
    'changed': False,
    'description': 'b',
}
assert settings.getDetails('test.c') == {
    'changed': False,
    'type': 'string',
}
assert settings.getDetails('test.d') == {
    'changed': False,
    'default': 42,
    'value': 42,
}

# redefining
assert settings.define('test.a', type='number', default=11) is None

assert settings.getDetails('test.a') == {
    'changed': False,
    'type': 'number',
    'default': 11,
    'value': 11,
}

assert settings.get('test.a') == 11
assert settings.set('test.a', 12) is None
assert settings.get('test.a') == 12
with assert_raises(LuaException):
    settings.set('test.a', 'text')
assert settings.get('test.a') == 12
assert settings.unset('test.a') is None
assert settings.get('test.a') == 11

assert settings.set('test.c', 'hello') is None

assert {'test.a', 'test.b', 'test.c', 'test.d'}.issubset(set(settings.getNames()))

assert settings.undefine('test.a') is None
assert settings.undefine('test.b') is None
assert settings.undefine('test.c') is None
assert settings.undefine('test.d') is None

assert 'test.c' in settings.getNames()
assert settings.get('test.c') == b'hello'
assert settings.getDetails('test.c') == {
    'changed': True,
    'value': b'hello',
}

assert settings.unset('test.c') is None

assert settings.get('test.c') is None
assert settings.getDetails('test.c') == {
    'changed': False,
}

assert {'test.a', 'test.b', 'test.c', 'test.d'} & set(settings.getNames()) == set()

assert settings.set('test.e', [9, 'text', False]) is None
assert settings.get('test.e') == {1: 9, 2: b'text', 3: False}  # TODO: fix this?
assert settings.clear() is None
assert settings.get('test.e') is None

fs.delete('.settings')

assert settings.load() is False
assert settings.save() is True
assert settings.load() is True

fs.delete('.settings')

assert settings.set('key', 84) is None

assert settings.save('sfile') is True
assert settings.load('sfile') is True

fs.delete('sfile')

print('Test finished successfully')
