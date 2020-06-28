import asyncio
from contextlib import contextmanager
from time import monotonic
from types import FunctionType

from computercraft.errors import LuaException


async def hello(api):
    await api.print('Hello world!')


async def id(api):
    await api.print('ID', await api.os.getComputerID())
    await api.print('Label', await api.os.getComputerLabel())
    await api.print('Version', await api.os.version())


async def move(api):
    for _ in range(4):
        await api.turtle.forward()
        await api.turtle.turnLeft()


async def t1(api):
    await api.print('kek')
    result = await api.raw_eval("return 'jopa\\njopa'")
    await api.print(f'{result}')
    raise IndexError


async def read(api):
    line = await api.read_line()
    await api.print(f'Entered line: {line}')


@contextmanager
def assert_raises(etype):
    try:
        yield
    except Exception as e:
        assert isinstance(e, etype)
    else:
        raise AssertionError(f'Exception of type {etype} was not raised')


@contextmanager
def assert_takes_time(at_least, at_most):
    t = monotonic()
    yield
    dt = monotonic() - t
    # print(at_least, '<=', dt, '<=', at_most)
    assert at_least <= dt <= at_most


class AnyInstanceOf:
    def __init__(self, cls):
        self.c = cls

    def __eq__(self, other):
        return isinstance(other, self.c)


async def step(api, text):
    await api.print(f'{text} [enter]')
    await api.read_line()


async def get_object_table(api, objname):
    r = await api.raw_eval(f"""
local r = {{}}
for k in pairs({objname}) do
    local t = type({objname}[k])
    if r[t] == nil then r[t] = {{}} end
    if t == 'number' or t == 'boolean' or t == 'string' then
        r[t][k] = {objname}[k]
    else
        r[t][k] = true
    end
end
return r""")
    assert r[0] is True
    return r[1]


def get_class_table(cls):
    items = {
        k: v for k, v in vars(cls).items()
        if not k.startswith('_')
    }
    nums = {
        k: v for k, v in items.items()
        if isinstance(v, (int, float))
    }
    methods = {
        k: True for k, v in items.items()
        if isinstance(v, FunctionType)
    }
    r = {}
    if nums:
        r['number'] = nums
    if methods:
        r['function'] = methods
    return r


async def test_colors_api(api):
    tbl = await get_object_table(api, 'colors')

    # use packRGB and unpackRGB
    del tbl['function']['rgb8']

    assert get_class_table(api.colors.__class__) == tbl

    cs = await api.colors.combine(
        api.colors.orange,
        api.colors.cyan,
        api.colors.pink,
        api.colors.brown,
    )
    assert isinstance(cs, int)
    cs = await api.colors.subtract(cs, api.colors.brown, api.colors.green)
    assert isinstance(cs, int)
    assert cs == await api.colors.combine(
        api.colors.orange,
        api.colors.cyan,
        api.colors.pink,
    )
    assert await api.colors.test(cs, api.colors.red) is False
    assert await api.colors.test(cs, api.colors.cyan) is True

    assert await api.colors.packRGB(0.7, 0.2, 0.6) == 0xb23399
    r, g, b = await api.colors.unpackRGB(0xb23399)
    assert 0.68 < r < 0.72
    assert 0.18 < g < 0.22
    assert 0.58 < b < 0.62

    await api.print('Test finished successfully')


async def test_disk_api(api):
    s = 'right'

    assert get_class_table(api.disk.__class__) \
        == await get_object_table(api, 'disk')

    await step(api, f'Make sure there is no disk drive at {s} side')

    assert await api.disk.isPresent(s) is False
    assert await api.disk.hasData(s) is False
    assert await api.disk.getMountPath(s) is None
    assert await api.disk.setLabel(s, 'text') is None
    assert await api.disk.getLabel(s) is None
    assert await api.disk.getID(s) is None
    assert await api.disk.hasAudio(s) is False
    assert await api.disk.getAudioTitle(s) is None
    assert await api.disk.playAudio(s) is None
    assert await api.disk.stopAudio(s) is None
    assert await api.disk.eject(s) is None

    await step(api, f'Place empty disk drive at {s} side')

    assert await api.disk.isPresent(s) is False
    assert await api.disk.hasData(s) is False
    assert await api.disk.getMountPath(s) is None
    assert await api.disk.setLabel(s, 'text') is None
    assert await api.disk.getLabel(s) is None
    assert await api.disk.getID(s) is None
    assert await api.disk.hasAudio(s) is False
    assert await api.disk.getAudioTitle(s) is False  # False instead None!
    assert await api.disk.playAudio(s) is None
    assert await api.disk.stopAudio(s) is None
    assert await api.disk.eject(s) is None

    await step(api, 'Put new CC diskette into disk drive')

    assert await api.disk.isPresent(s) is True
    assert await api.disk.hasData(s) is True
    assert isinstance(await api.disk.getMountPath(s), str)
    assert isinstance(await api.disk.getID(s), int)

    assert await api.disk.getLabel(s) is None
    assert await api.disk.setLabel(s, 'label') is None
    assert await api.disk.getLabel(s) == 'label'
    assert await api.disk.setLabel(s, None) is None
    assert await api.disk.getLabel(s) is None

    assert await api.disk.hasAudio(s) is False
    assert await api.disk.getAudioTitle(s) is None
    assert await api.disk.playAudio(s) is None
    assert await api.disk.stopAudio(s) is None

    assert await api.disk.eject(s) is None

    await step(api, 'Put any audio disk into disk drive')

    assert await api.disk.isPresent(s) is True
    assert await api.disk.hasData(s) is False
    assert await api.disk.getMountPath(s) is None
    assert await api.disk.getID(s) is None
    assert await api.disk.hasAudio(s) is True

    label = await api.disk.getAudioTitle(s)
    assert isinstance(label, str)
    assert label != 'label'
    await api.print(f'Label is {label}')
    assert await api.disk.getLabel(s) == label
    with assert_raises(LuaException):
        assert await api.disk.setLabel(s, 'label') is None
    with assert_raises(LuaException):
        assert await api.disk.setLabel(s, None) is None
    # no effect
    assert await api.disk.getLabel(s) == label

    assert await api.disk.playAudio(s) is None

    await step(api, 'Audio must be playing now')

    assert await api.disk.stopAudio(s) is None
    assert await api.disk.eject(s) is None

    await api.print('Test finished successfully')


async def test_commands_api(api):
    assert get_class_table(api.commands.__class__) \
        == await get_object_table(api, 'commands.native')

    xyz = await api.commands.getBlockPosition()

    assert len(xyz) == 3
    for c in xyz:
        assert isinstance(c, int)

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
            'ComputerId': AnyInstanceOf(int),
            'id': 'computercraft:command_computer',
            'On': 1,
        },
    }

    assert await api.commands.getBlockInfo(*xyz) == expected_binfo
    assert await api.commands.getBlockInfos(*xyz, *xyz) == [expected_binfo]

    cmdlist = await api.commands.list()

    assert len(cmdlist) > 0
    for c in cmdlist:
        assert isinstance(c, str)

    assert await api.commands.exec('say Hello!') == (True, [], AnyInstanceOf(int))

    d = await api.commands.exec('tp hajejndlasksdkelefsns fjeklaskslekffjslas')
    assert d[0] is False

    d = await api.commands.exec('difficulty')
    assert d[0] is True
    assert len(d[1]) == 1
    assert d[1][0].startswith('The difficulty is ')
    assert isinstance(d[2], int)

    await api.print('Test finished successfully')


async def test_fs_api(api):
    assert get_class_table(api.fs.__class__) \
        == await get_object_table(api, 'fs')

    for name in ('tdir', 'tfile'):
        if await api.fs.exists(name):
            await api.fs.delete(name)

    assert await api.fs.makeDir('tdir') is None
    async with api.fs.open('tfile', 'w') as f:
        await f.writeLine('textline')

    dlist = set(await api.fs.list('.'))

    assert {'tdir', 'tfile', 'rom'}.issubset(dlist)
    assert await api.fs.list('tdir') == []

    capacity = await api.fs.getCapacity('.')
    free = await api.fs.getFreeSpace('.')
    assert isinstance(capacity, int)
    assert isinstance(free, int)
    assert free < capacity
    assert free > 0
    assert capacity > 0

    assert await api.fs.exists('tdir') is True
    assert await api.fs.exists('tfile') is True
    assert await api.fs.exists('doesnotexist') is False

    assert await api.fs.isDir('tdir') is True
    assert await api.fs.isDir('tfile') is False
    assert await api.fs.isDir('doesnotexist') is False

    assert await api.fs.isReadOnly('rom') is True
    assert await api.fs.isReadOnly('tdir') is False
    assert await api.fs.isReadOnly('tfile') is False
    assert await api.fs.isReadOnly('doesnotexist') is False

    assert await api.fs.getDrive('rom') == 'rom'
    assert await api.fs.getDrive('tdir') == 'hdd'
    assert await api.fs.getDrive('tfile') == 'hdd'
    assert await api.fs.getDrive('doesnotexist') is None

    assert await api.fs.isDriveRoot('/') is True
    assert await api.fs.isDriveRoot('rom') is True
    assert await api.fs.isDriveRoot('tdir') is False
    assert await api.fs.isDriveRoot('tfile') is False
    assert await api.fs.isDriveRoot('doesnotexist') is True  # wtf?

    assert await api.fs.getName('a/b/c/d') == 'd'
    assert await api.fs.getName('a/b/c/') == 'c'
    assert await api.fs.getName('/a/b/c/d') == 'd'
    assert await api.fs.getName('///a/b/c/d') == 'd'
    assert await api.fs.getName('') == 'root'  # wtf?
    assert await api.fs.getName('/') == 'root'
    assert await api.fs.getName('///') == 'root'
    assert await api.fs.getName('.') == 'root'
    assert await api.fs.getName('..') == '..'
    assert await api.fs.getName('../../..') == '..'

    assert await api.fs.getDir('a/b/c/d') == 'a/b/c'
    assert await api.fs.getDir('a/b/c/') == 'a/b'
    assert await api.fs.getDir('/a/b/c/d') == 'a/b/c'
    assert await api.fs.getDir('///a/b/c/d') == 'a/b/c'
    assert await api.fs.getDir('') == '..'
    assert await api.fs.getDir('/') == '..'
    assert await api.fs.getDir('///') == '..'
    assert await api.fs.getDir('.') == '..'
    assert await api.fs.getDir('..') == ''
    assert await api.fs.getDir('../../..') == '../..'

    assert await api.fs.combine('a', 'b') == 'a/b'
    assert await api.fs.combine('a/', 'b') == 'a/b'
    assert await api.fs.combine('a//', 'b') == 'a/b'
    assert await api.fs.combine('a/', '/b') == 'a/b'
    assert await api.fs.combine('a/b/c', '..') == 'a/b'
    assert await api.fs.combine('a/b/c', '../..') == 'a'
    assert await api.fs.combine('a/b/c', '../../..') == ''
    assert await api.fs.combine('a/b/c', '../../../..') == '..'
    assert await api.fs.combine('a/b/c', '../../../../..') == '../..'
    assert await api.fs.combine('/a/b/c', '../../../../..') == '../..'
    assert await api.fs.combine('a/b/c', '////') == 'a/b/c'
    assert await api.fs.combine('a/b/c', '.') == 'a/b/c'
    assert await api.fs.combine('a/b/c', './.') == 'a/b/c'
    assert await api.fs.combine('a/b/c', './../.') == 'a/b'

    assert await api.fs.getSize('tfile') == 9
    assert await api.fs.getSize('tdir') == 0
    with assert_raises(LuaException):
        await api.fs.getSize('doesnotexist')

    assert await api.fs.move('tfile', 'tdir/apple') is None
    assert await api.fs.list('tdir') == ['apple']
    assert await api.fs.copy('tdir/apple', 'tdir/banana') is None
    assert await api.fs.list('tdir/') == ['apple', 'banana']
    assert await api.fs.copy('tdir/apple', 'tdir/cherry') is None

    assert await api.fs.getSize('tdir') == 0

    dlist = set(await api.fs.find('*'))
    assert 'tdir' in dlist
    assert 'rom' in dlist
    assert 'tfile' not in dlist
    assert 'tdir/apple' not in dlist

    dlist = set(await api.fs.find('tdir/*'))
    assert dlist == {'tdir/apple', 'tdir/banana', 'tdir/cherry'}

    dlist = set(await api.fs.find('tdir/*a*'))
    assert dlist == {'tdir/apple', 'tdir/banana'}

    dlist = set(await api.fs.find('**'))
    assert 'tdir' in dlist
    assert 'tdir/apple' not in dlist  # not recursive

    dlist = set(await api.fs.list(''))
    assert 'tfile' not in dlist
    assert 'tdir' in dlist
    assert 'rom' in dlist

    dlist = set(await api.fs.list('tdir'))
    assert dlist == {'apple', 'banana', 'cherry'}

    assert await api.fs.attributes('tdir/banana') == {
        'created': AnyInstanceOf(int),
        'modification': AnyInstanceOf(int),
        'isDir': False,
        'size': 9,
    }
    assert await api.fs.attributes('tdir') == {
        'created': AnyInstanceOf(int),
        'modification': AnyInstanceOf(int),
        'isDir': True,
        'size': 0,
    }
    with assert_raises(LuaException):
        await api.fs.attributes('doesnotexist')

    assert await api.fs.complete('ba', 'tdir') == ['nana']
    assert await api.fs.complete('ap', 'tdir') == ['ple']
    assert await api.fs.complete('c', 'tdir') == ['herry']
    assert await api.fs.complete('td', '') == ['ir/', 'ir']
    assert await api.fs.complete('td', '', includeDirs=True) == ['ir/', 'ir']
    assert await api.fs.complete('td', '', includeDirs=False) == ['ir/']  # wtf?
    assert await api.fs.complete('ap', 'tdir', includeFiles=True) == ['ple']
    assert await api.fs.complete('ap', 'tdir', includeFiles=False) == []

    assert await api.fs.getSize('tdir/banana') == 9
    async with api.fs.open('tdir/banana', 'r') as f:
        assert await get_object_table(api, f._API) == {'function': {
            'close': True,
            'read': True,
            'readLine': True,
            'readAll': True,
        }}
        assert await f.read(4) == 'text'
        assert await f.readLine() == 'line'
        assert await f.read(1) is None
        assert await f.readLine() is None
        assert await f.readAll() == ''
        assert await f.readAll() == ''
    assert await api.fs.getSize('tdir/banana') == 9
    async with api.fs.open('tdir/banana', 'a') as f:
        assert await get_object_table(api, f._API) == {'function': {
            'close': True,
            'write': True,
            'writeLine': True,
            'flush': True,
        }}
        assert await f.write('x') is None
    assert await api.fs.getSize('tdir/banana') == 10
    async with api.fs.open('tdir/banana', 'w') as f:
        pass
    assert await api.fs.getSize('tdir/banana') == 0  # truncate
    async with api.fs.open('tdir/banana', 'w') as f:
        assert await get_object_table(api, f._API) == {'function': {
            'close': True,
            'write': True,
            'writeLine': True,
            'flush': True,
        }}
        assert await f.write('Bro') is None
        assert await f.writeLine('wn fox jumps') is None
        assert await api.fs.getSize('tdir/banana') == 0  # changes are not on a disk
        assert await f.flush() is None
        assert await api.fs.getSize('tdir/banana') == len('Brown fox jumps\n')
        assert await f.write('ov') is None
        assert await f.write('er ') is None
        assert await f.write('a lazy') is None
        assert await f.writeLine(' dog.') is None
    assert await api.fs.getSize('tdir/banana') > 9
    async with api.fs.open('tdir/banana', 'r') as f:
        assert await f.readAll() == 'Brown fox jumps\nover a lazy dog.'  # no newline?
    with assert_raises(LuaException):
        async with api.fs.open('tdir/banana', 'rw') as f:
            pass

    assert await api.fs.exists('tdir/banana') is True

    assert await api.fs.delete('tdir') is None
    assert await api.fs.delete('tfile') is None
    assert await api.fs.delete('doesnotexist') is None

    assert await api.fs.exists('tdir/banana') is False

    await api.print('Test finished successfully')


async def test_gps_basic_computer(api):
    assert get_class_table(api.gps.__class__) \
        == await get_object_table(api, 'gps')

    assert await api.gps.locate() is None

    await step(api, 'Attach wireless modem to computer')

    assert await api.gps.locate() is None

    assert await api.gps.locate(debug=True) is None

    assert await api.gps.locate(timeout=5, debug=True) is None

    await api.print('Test finished successfully')


async def test_gps_command_computer(api):
    assert get_class_table(api.gps.__class__) \
        == await get_object_table(api, 'gps')

    assert await api.gps.locate() == (
        AnyInstanceOf(int),
        AnyInstanceOf(int),
        AnyInstanceOf(int),
    )

    await api.print('Test finished successfully')


async def test_keys_api(api):
    a = await api.keys.getCode('a')
    space = await api.keys.getCode('space')
    enter = await api.keys.getCode('enter')
    assert await api.keys.getCode('doesnotexist') is None
    assert await api.keys.getCode('getName') is None
    assert isinstance(a, int)
    assert isinstance(space, int)
    assert isinstance(enter, int)

    assert await api.keys.getName(a) == 'a'
    assert await api.keys.getName(space) == 'space'
    assert await api.keys.getName(enter) == 'enter'

    # for i in range(255):
    #     print(i, await api.keys.getName(i))

    await api.print('Test finished successfully')


async def test_help_api(api):
    assert get_class_table(api.help.__class__) \
        == await get_object_table(api, 'help')

    await api.help.setPath('/rom/help')

    assert await api.help.path() == '/rom/help'

    assert await api.help.lookup('disk') == 'rom/help/disk.txt'
    assert await api.help.lookup('abracadabra') is None

    ts = await api.help.topics()
    assert isinstance(ts, list)
    assert len(ts) > 2
    # print(ts)
    assert 'disk' in ts

    assert await api.help.completeTopic('di') == ['sk']
    assert await api.help.completeTopic('abracadabra') == []

    assert await api.help.setPath('/kek') is None
    assert await api.help.path() == '/kek'
    assert await api.help.topics() == ['index']
    assert await api.help.setPath('/rom/help') is None

    await api.print('Test finished successfully')


async def test_reboot(api):
    assert await api.os.reboot() is None
    await api.print('Test finished successfully')


async def test_shutdown(api):
    assert await api.os.shutdown() is None
    await api.print('Test finished successfully')


async def test_os_api(api):
    tbl = await get_object_table(api, 'os')

    # use methods with get*
    del tbl['function']['computerID']
    del tbl['function']['computerLabel']

    # use captureEvent
    del tbl['function']['pullEvent']
    del tbl['function']['pullEventRaw']

    # we are in python world, loading lua modules is useless
    del tbl['function']['loadAPI']
    del tbl['function']['unloadAPI']

    # remove complex date formatting function in favor of python stdlib
    del tbl['function']['date']

    tbl['function']['captureEvent'] = True

    assert get_class_table(api.os.__class__) == tbl

    with assert_takes_time(1.5, 3):
        async with api.os.captureEvent('timer') as timer_queue:
            timer_id = await api.os.startTimer(2)
            async for etid, in timer_queue:
                if etid == timer_id:
                    await api.print('Timer reached')
                    break

    timer_id = await api.os.startTimer(20)
    assert isinstance(timer_id, int)
    assert await api.os.cancelTimer(timer_id) is None
    assert await api.os.cancelTimer(timer_id) is None

    alarm_id = await api.os.setAlarm(0.0)
    assert isinstance(alarm_id, int)
    assert await api.os.cancelAlarm(alarm_id) is None
    assert await api.os.cancelAlarm(alarm_id) is None

    with assert_takes_time(1.5, 3):
        assert await api.os.sleep(2) is None

    assert (await api.os.version()).startswith('CraftOS ')
    assert isinstance(await api.os.getComputerID(), int)

    assert await api.os.setComputerLabel(None) is None
    assert await api.os.getComputerLabel() is None
    assert await api.os.setComputerLabel('altair') is None
    assert await api.os.getComputerLabel() == 'altair'
    assert await api.os.setComputerLabel(None) is None
    assert await api.os.getComputerLabel() is None

    assert isinstance(await api.os.epoch(), int)
    assert isinstance(await api.os.day(), int)
    assert isinstance(await api.os.time(), (int, float))
    assert isinstance(await api.os.clock(), (int, float))

    # TODO: run method

    await api.print('Test finished successfully')


async def test_parallel(api):
    with assert_takes_time(1.5, 3):
        # Since os.sleep is mostly waiting for events, it doesn't block execution of parallel threads
        # and this snippet takes approximately 2 seconds to complete.
        await asyncio.gather(api.os.sleep(2), api.os.sleep(2))

    await api.print('Test finished successfully')


async def term_step(api, text):
    for color in api.colors:
        r, g, b = await api.term.nativePaletteColor(color)
        await api.term.setPaletteColor(color, r, g, b)
    await api.term.setBackgroundColor(api.colors.black)
    await api.term.setTextColor(api.colors.white)
    await api.term.clear()
    await api.term.setCursorPos(1, 1)
    await api.term.setCursorBlink(True)
    await step(api, text)


async def test_term_api(api):
    from computercraft.subapis.mixins import TermMixin

    tbl = await get_object_table(api, 'term')

    # not defined in TermMixin
    del tbl['function']['redirect']
    del tbl['function']['current']
    del tbl['function']['native']

    # remove British method names to make API lighter
    del tbl['function']['getBackgroundColour']
    del tbl['function']['getPaletteColour']
    del tbl['function']['getTextColour']
    del tbl['function']['isColour']
    del tbl['function']['nativePaletteColour']
    del tbl['function']['setBackgroundColour']
    del tbl['function']['setPaletteColour']
    del tbl['function']['setTextColour']

    assert get_class_table(TermMixin) == tbl

    await step(api, 'Detach all monitors\nUse advanced computer for colors\nScreen will be cleared')

    assert await api.term.getSize() == (51, 19)
    assert await api.term.isColor() is True
    assert await api.term.clear() is None
    assert await api.term.setCursorPos(1, 1) is None
    assert await api.term.getCursorPos() == (1, 1)
    assert await api.term.write('Alpha') is None
    assert await api.term.getCursorPos() == (6, 1)
    assert await api.term.setCursorBlink(False) is None
    assert await api.term.getCursorBlink() is False
    assert await api.term.setCursorBlink(True) is None
    assert await api.term.getCursorBlink() is True
    await asyncio.sleep(2)

    await term_step(api, 'You must have seen word Alpha with blinking cursor')

    assert await api.term.clear() is None
    for offs, (tc, bc) in enumerate((
        (api.colors.lime, api.colors.green),
        (api.colors.yellow, api.colors.brown),
        (api.colors.red, api.colors.orange),
    ), start=1):
        assert await api.term.setTextColor(tc) is None
        assert await api.term.getTextColor() == tc
        assert await api.term.setBackgroundColor(bc) is None
        assert await api.term.getBackgroundColor() == bc
        assert await api.term.setCursorPos(offs * 2, offs) is None
        assert await api.term.getCursorPos() == (offs * 2, offs)
        assert await api.term.write('text with colors') is None
    assert await api.term.setBackgroundColor(api.colors.black) is None
    await asyncio.sleep(1)
    for i in range(3):
        assert await api.term.scroll(-2) is None
        await asyncio.sleep(0.5)
    for i in range(6):
        assert await api.term.scroll(1) is None
        await asyncio.sleep(0.25)

    await term_step(api, 'You must have seen three texts with different colors scrolling')

    assert await api.term.clear() is None
    for i in range(1, 10):
        assert await api.term.setCursorPos(1, i) is None
        assert await api.term.write((str(i) + '  ') * 10) is None
    await asyncio.sleep(2)
    for i in range(2, 10, 2):
        assert await api.term.setCursorPos(1, i) is None
        assert await api.term.clearLine() is None
    await asyncio.sleep(2)

    await term_step(api, 'You must have seen some lines disappearing')

    assert await api.term.clear() is None
    assert await api.term.setCursorPos(1, 1) is None
    assert await api.term.blit(
        'rainbowrainbow',
        'e14d3ba0000000',
        'fffffffe14d3ba',
    ) is None
    await asyncio.sleep(3)

    await term_step(api, 'You must have seen per-letter colored text')

    assert await api.term.setBackgroundColor(api.colors.white) is None
    assert await api.term.clear() is None
    assert await api.term.setCursorPos(1, 1) is None
    for i, color in enumerate(api.colors):
        await api.term.setPaletteColor(color, i / 15, 0, 0)
    assert await api.term.blit(
        ' redtextappears!',
        '0123456789abcdef',
        '0000000000000000',
    ) is None
    await asyncio.sleep(3)

    await term_step(api, 'You must have seen different shades of red made using palettes')

    await api.print('Test finished successfully')
