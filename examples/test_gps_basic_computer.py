from cc import import_file, gps

_lib = import_file('_lib.py', __file__)


assert _lib.get_class_table(gps) == _lib.get_object_table('gps')

assert gps.locate() is None

_lib.step('Attach wireless modem to computer')

assert gps.locate() is None

assert gps.locate(debug=True) is None

assert gps.locate(timeout=5, debug=True) is None

print('Test finished successfully')
