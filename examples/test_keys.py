from cc import keys


a = keys.getCode('a')
space = keys.getCode('space')
enter = keys.getCode('enter')
assert keys.getCode('doesnotexist') is None
assert keys.getCode('getName') is None
assert isinstance(a, int)
assert isinstance(space, int)
assert isinstance(enter, int)

assert keys.getName(a) == 'a'
assert keys.getName(space) == 'space'
assert keys.getName(enter) == 'enter'

# for i in range(255):
#     print(i, keys.getName(i))

print('Test finished successfully')
