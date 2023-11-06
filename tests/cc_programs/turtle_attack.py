from cc import import_file, turtle

_lib = import_file('_lib.py', __file__)


_lib.step(
    'NOTE: this test is unreliable\n'
    'Build 1x1x1 stone cage in front of turtle\n'
    'Spawn here a chicken',
)

assert turtle.attack() is True
assert type(turtle.attack()) is bool
assert turtle.attack() is False

_lib.step(
    'Build 1x1x1 stone cage below turtle\n'
    'Spawn here a chicken',
)

assert turtle.attackDown() is True
assert type(turtle.attackDown()) is bool
assert turtle.attackDown() is False

_lib.step(
    'Build 1x1x1 stone cage above turtle\n'
    'Spawn here a chicken',
)

assert turtle.attackUp() is True
assert type(turtle.attackUp()) is bool
assert turtle.attackUp() is False

print('Test finished successfully')
