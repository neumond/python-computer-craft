from cc import commands


class AnyInstanceOf:
    def __init__(self, cls):
        self.c = cls

    def __eq__(self, other):
        return isinstance(other, self.c)


print('Run this test on command computer')

xyz = commands.getBlockPosition()
assert xyz == (
    AnyInstanceOf(int),
    AnyInstanceOf(int),
    AnyInstanceOf(int),
)

expected_binfo = {
    'state': {
        'state': AnyInstanceOf(str),
        'facing': AnyInstanceOf(str),
    },
    'name': 'computercraft:computer_command',
    'nbt': {
        'x': xyz[0],
        'y': xyz[1],
        'z': xyz[2],
        'ForgeCaps': {},
        'ComputerId': AnyInstanceOf(int),
        'id': 'computercraft:computer_command',
        'On': 1,
    },
    'tags': {'computercraft:computer': True},
}

assert commands.getBlockInfo(*xyz) == expected_binfo
assert commands.getBlockInfos(*xyz, *xyz) == [expected_binfo]

cmdlist = commands.list()

assert len(cmdlist) > 0
for c in cmdlist:
    assert isinstance(c, str)

assert commands.exec('say Hello!') == (True, [], AnyInstanceOf(int))

d = commands.exec('tp hajejndlasksdkelefsns fjeklaskslekffjslas')
assert d[0] is False

d = commands.exec('difficulty')
assert d[0] is True
assert len(d[1]) == 1
assert d[1][0].startswith('The difficulty is ')
assert isinstance(d[2], int)

print('Test finished successfully')
