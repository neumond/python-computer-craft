from oc import os


print(os.date())
c = os.clock()
assert c >= 0
t = os.time()
assert t >= 0

assert os.sleep(2) is None

assert os.clock() >= c
assert os.time() >= t

os.exit()
print('unreachable')
