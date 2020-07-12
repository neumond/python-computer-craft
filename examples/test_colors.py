from cc import import_file, colors

_lib = import_file('_lib.py', __file__)


tbl = _lib.get_object_table('colors')

# use packRGB and unpackRGB
del tbl['function']['rgb8']

tbl['function']['iter_colors'] = True

assert _lib.get_class_table(colors) == tbl

cs = colors.combine(
    colors.orange,
    colors.cyan,
    colors.pink,
    colors.brown,
)
assert isinstance(cs, int)
cs = colors.subtract(cs, colors.brown, colors.green)
assert isinstance(cs, int)
assert cs == colors.combine(
    colors.orange,
    colors.cyan,
    colors.pink,
)
assert colors.test(cs, colors.red) is False
assert colors.test(cs, colors.cyan) is True

assert colors.packRGB(0.7, 0.2, 0.6) == 0xb23399
r, g, b = colors.unpackRGB(0xb23399)
assert 0.68 < r < 0.72
assert 0.18 < g < 0.22
assert 0.58 < b < 0.62

print('Test finished successfully')
