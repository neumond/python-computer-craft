from cc import import_file, gps

_lib = import_file('_lib.py', __file__)


assert _lib.get_class_table(gps) == _lib.get_object_table('gps')

assert gps.locate() == (
    _lib.AnyInstanceOf(int),
    _lib.AnyInstanceOf(int),
    _lib.AnyInstanceOf(int),
)

print('Test finished successfully')
