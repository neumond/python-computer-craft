from cc import import_file, commands

_lib = import_file('_lib.py', __file__)
AnyInstanceOf = _lib.AnyInstanceOf


tbl = _lib.get_object_table('commands.native')
# remove in favor of exec
del tbl['function']['execAsync']
assert _lib.get_class_table(commands) == tbl

xyz = commands.getBlockPosition()

assert len(xyz) == 3
for c in xyz:
    assert isinstance(c, int)

# TODO: decode bytes?
expected_binfo = {
    b'state': {
        b'state': AnyInstanceOf(bytes),
        b'facing': AnyInstanceOf(bytes),
    },
    b'name': b'computercraft:computer_command',
    b'nbt': {
        b'x': xyz[0],
        b'y': xyz[1],
        b'z': xyz[2],
        b'ComputerId': AnyInstanceOf(int),
        b'id': b'computercraft:computer_command',
        b'On': 1,
    },
    b'tags': {},
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
