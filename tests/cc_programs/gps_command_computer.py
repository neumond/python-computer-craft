from cc import gps


print('Run this test on command computer')
pos = gps.locate()
assert isinstance(pos, tuple)
assert len(pos) == 3
assert all(isinstance(x, int) for x in pos)
print('Position is', pos)
print('Test finished successfully')
