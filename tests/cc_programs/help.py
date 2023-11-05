from cc import help


help.setPath('/rom/help')

assert help.path() == '/rom/help'

assert help.lookup('disk') == 'rom/help/disk.txt'
assert help.lookup('abracadabra') is None

ts = help.topics()
assert isinstance(ts, list)
assert len(ts) > 2
assert 'disk' in ts

assert help.completeTopic('di') == ['sk']
assert help.completeTopic('abracadabra') == []

assert help.setPath('/kek') is None
assert help.path() == '/kek'
assert help.topics() == ['index']
assert help.setPath('/rom/help') is None

print('Test finished successfully')
