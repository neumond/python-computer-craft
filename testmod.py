import asyncio
import random
from contextlib import contextmanager, AsyncExitStack
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
    result = await api.eval("return 'jopa\\njopa'")
    await api.print(f'{result}')
    raise IndexError


async def read(api):
    line = await api.read_line()
    await api.print(f'Entered line: {line}')


@contextmanager
def assert_raises(etype, message=None):
    try:
        yield
    except Exception as e:
        assert isinstance(e, etype)
        if message is not None:
            assert e.args == (message, )
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
    r = await api.eval(f"""
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
    assert len(r) == 1
    return r[0]


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


def get_multiclass_table(*cls):
    result = {}
    for c in cls:
        for k, v in get_class_table(c).items():
            result.setdefault(k, {}).update(v)
    return result


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
    tbl = await get_object_table(api, 'commands.native')
    # remove in favor of exec
    del tbl['function']['execAsync']
    assert get_class_table(api.commands.__class__) == tbl

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
            'id': 'computercraft:computer_command',
            'On': 1,
        },
        'tags': {},
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
        assert await get_object_table(api, f.get_expr_code()) == {'function': {
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
        assert await get_object_table(api, f.get_expr_code()) == {'function': {
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
        assert await get_object_table(api, f.get_expr_code()) == {'function': {
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
            async for etid, *_ in timer_queue:
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

    assert await api.os.run({}, 'rom/programs/fun/hello.lua') is True

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


async def test_settings_api(api):
    tbl = await get_object_table(api, 'settings')
    assert get_class_table(api.settings.__class__) == tbl

    await step(api, 'Settings will be cleared')

    assert await api.settings.clear() is None
    # names are not empty, there are system settings
    assert isinstance(await api.settings.getNames(), list)

    assert await api.settings.define('test.a') is None
    assert await api.settings.define('test.b', description='b') is None
    assert await api.settings.define('test.c', type='string') is None
    assert await api.settings.define('test.d', default=42) is None

    assert await api.settings.getDetails('test.a') == {
        'changed': False,
    }
    assert await api.settings.getDetails('test.b') == {
        'changed': False,
        'description': 'b',
    }
    assert await api.settings.getDetails('test.c') == {
        'changed': False,
        'type': 'string',
    }
    assert await api.settings.getDetails('test.d') == {
        'changed': False,
        'default': 42,
        'value': 42,
    }

    # redefining
    assert await api.settings.define('test.a', type='number', default=11) is None

    assert await api.settings.getDetails('test.a') == {
        'changed': False,
        'type': 'number',
        'default': 11,
        'value': 11,
    }

    assert await api.settings.get('test.a') == 11
    assert await api.settings.set('test.a', 12) is None
    assert await api.settings.get('test.a') == 12
    with assert_raises(LuaException):
        await api.settings.set('test.a', 'text')
    assert await api.settings.get('test.a') == 12
    assert await api.settings.unset('test.a') is None
    assert await api.settings.get('test.a') == 11

    assert await api.settings.set('test.c', 'hello') is None

    assert {'test.a', 'test.b', 'test.c', 'test.d'}.issubset(set(await api.settings.getNames()))

    assert await api.settings.undefine('test.a') is None
    assert await api.settings.undefine('test.b') is None
    assert await api.settings.undefine('test.c') is None
    assert await api.settings.undefine('test.d') is None

    assert 'test.c' in await api.settings.getNames()
    assert await api.settings.get('test.c') == 'hello'
    assert await api.settings.getDetails('test.c') == {
        'changed': True,
        'value': 'hello',
    }

    assert await api.settings.unset('test.c') is None

    assert await api.settings.get('test.c') is None
    assert await api.settings.getDetails('test.c') == {
        'changed': False,
    }

    assert {'test.a', 'test.b', 'test.c', 'test.d'} & set(await api.settings.getNames()) == set()

    assert await api.settings.set('test.e', [9, 'text', False]) is None
    assert await api.settings.get('test.e') == [9, 'text', False]
    assert await api.settings.clear() is None
    assert await api.settings.get('test.e') is None

    await api.fs.delete('.settings')

    assert await api.settings.load() is False
    assert await api.settings.save() is True
    assert await api.settings.load() is True

    await api.fs.delete('.settings')

    assert await api.settings.set('key', 84) is None

    assert await api.settings.save('sfile') is True
    assert await api.settings.load('sfile') is True

    await api.fs.delete('sfile')

    await api.print('Test finished successfully')


async def test_redstone_api(api):
    tbl = await get_object_table(api, 'redstone')

    # remove British method names to make API lighter
    del tbl['function']['getAnalogueInput']
    del tbl['function']['getAnalogueOutput']
    del tbl['function']['setAnalogueOutput']

    assert get_class_table(api.redstone.__class__) == tbl

    assert set(await api.redstone.getSides()) == {'top', 'bottom', 'front', 'back', 'left', 'right'}

    await step(api, 'Remove all the redstone from sides of computer')

    side = 'top'

    assert await api.redstone.setOutput(side, True) is None
    assert await api.redstone.getOutput(side) is True
    assert await api.redstone.getAnalogOutput(side) == 15
    assert await api.redstone.setOutput(side, False) is None
    assert await api.redstone.getOutput(side) is False
    assert await api.redstone.getAnalogOutput(side) == 0

    assert await api.redstone.setAnalogOutput(side, 7) is None
    assert await api.redstone.getAnalogOutput(side) == 7
    assert await api.redstone.getOutput(side) is True
    assert await api.redstone.setAnalogOutput(side, 15) is None
    assert await api.redstone.getAnalogOutput(side) == 15
    assert await api.redstone.setAnalogOutput(side, 0) is None
    assert await api.redstone.getAnalogOutput(side) == 0
    assert await api.redstone.getOutput(side) is False

    assert await api.redstone.getInput(side) is False
    assert await api.redstone.getAnalogInput(side) == 0

    await step(api, f'Put redstone block on {side} side of computer')

    assert await api.redstone.getInput(side) is True
    assert await api.redstone.getAnalogInput(side) > 0

    await step(api, f'Remove redstone block\nPut piston on {side} side of computer')

    assert await api.redstone.getInput(side) is False
    assert await api.redstone.getAnalogInput(side) == 0
    assert await api.redstone.setOutput(side, True) is None
    await asyncio.sleep(2)
    assert await api.redstone.setOutput(side, False) is None

    await api.print('Piston must have been activated\nRemove piston')

    await api.print('Test finished successfully')


async def test_peripheral_api(api):
    tbl = await get_object_table(api, 'peripheral')

    # use wrap
    del tbl['function']['getMethods']
    del tbl['function']['call']

    # TODO: support these methods
    del tbl['function']['getName']
    del tbl['function']['find']

    assert get_class_table(api.peripheral.__class__) == tbl

    await step(api, 'Remove all peripherals')

    side = 'top'

    assert await api.peripheral.getNames() == []
    assert await api.peripheral.getType(side) is None
    assert await api.peripheral.isPresent(side) is False
    assert await api.peripheral.wrap(side) is None

    await step(api, f'Put disk drive on {side} side of computer')

    assert await api.peripheral.getNames() == [side]
    assert await api.peripheral.getType(side) == 'drive'
    assert await api.peripheral.isPresent(side) is True
    d = await api.peripheral.wrap(side)
    assert d is not None
    assert await d.isDiskPresent() is False

    await api.print('Remove disk drive')

    await api.print('Test finished successfully')


async def test_disk_peripheral(api):
    side = 'left'

    await step(api, f'Put empty disk drive on {side} side of computer')

    d = await api.peripheral.wrap(side)
    assert d is not None

    from computercraft.subapis.peripheral import CCDrive
    tbl = await get_object_table(api, f'peripheral.wrap("{side}")')
    assert get_class_table(CCDrive) == tbl

    assert await d.isDiskPresent() is False
    assert await d.hasData() is False
    assert await d.getMountPath() is None
    assert await d.setDiskLabel('text') is None
    assert await d.getDiskLabel() is None
    assert await d.getDiskID() is None
    assert await d.hasAudio() is False
    assert await d.getAudioTitle() is False  # False instead None!
    assert await d.playAudio() is None
    assert await d.stopAudio() is None
    assert await d.ejectDisk() is None

    await step(api, 'Put new CC diskette into disk drive')

    assert await d.isDiskPresent() is True
    assert await d.hasData() is True
    assert isinstance(await d.getMountPath(), str)
    assert isinstance(await d.getDiskID(), int)

    assert await d.getDiskLabel() is None
    assert await d.setDiskLabel('label') is None
    assert await d.getDiskLabel() == 'label'
    assert await d.setDiskLabel(None) is None
    assert await d.getDiskLabel() is None

    assert await d.hasAudio() is False
    assert await d.getAudioTitle() is None
    assert await d.playAudio() is None
    assert await d.stopAudio() is None

    assert await d.ejectDisk() is None

    await step(api, 'Put any audio disk into disk drive')

    assert await d.isDiskPresent() is True
    assert await d.hasData() is False
    assert await d.getMountPath() is None
    assert await d.getDiskID() is None
    assert await d.hasAudio() is True

    label = await d.getAudioTitle()
    assert isinstance(label, str)
    assert label != 'label'
    await api.print(f'Label is {label}')
    assert await d.getDiskLabel() == label
    with assert_raises(LuaException):
        assert await d.setDiskLabel('label') is None
    with assert_raises(LuaException):
        assert await d.setDiskLabel(None) is None
    # no effect
    assert await d.getDiskLabel() == label

    assert await d.playAudio() is None

    await step(api, 'Audio must be playing now')

    assert await d.stopAudio() is None
    assert await d.ejectDisk() is None

    await api.print('Test finished successfully')


async def test_monitor_peripheral(api):
    side = 'left'

    await step(
        api,
        'Use advanced computer and monitor for colors\n'
        f'Place single block monitor on {side} side of computer',
    )

    m = await api.peripheral.wrap(side)
    assert m is not None

    from computercraft.subapis.peripheral import CCMonitor
    from computercraft.subapis.mixins import TermMixin

    tbl = await get_object_table(api, f'peripheral.wrap("{side}")')

    # remove British method names to make API lighter
    del tbl['function']['getBackgroundColour']
    del tbl['function']['getPaletteColour']
    del tbl['function']['getTextColour']
    del tbl['function']['isColour']
    del tbl['function']['setBackgroundColour']
    del tbl['function']['setPaletteColour']
    del tbl['function']['setTextColour']
    # NOTE: peripheral doesn't have nativePaletteColor method

    assert get_multiclass_table(TermMixin, CCMonitor) == tbl

    assert await m.getSize() == (7, 5)
    assert await m.isColor() is True
    assert await m.setTextColor(api.colors.white) is None
    assert await m.setBackgroundColor(api.colors.black) is None
    assert await m.clear() is None
    assert await m.setCursorPos(1, 1) is None
    assert await m.getCursorPos() == (1, 1)
    assert await m.write('Alpha') is None
    assert await m.getCursorPos() == (6, 1)
    assert await m.setCursorBlink(False) is None
    assert await m.getCursorBlink() is False
    assert await m.setCursorBlink(True) is None
    assert await m.getCursorBlink() is True

    await step(api, 'You must have seen word Alpha with blinking cursor')

    assert await m.clear() is None
    assert await m.setCursorBlink(False) is None
    for offs, (tc, bc) in enumerate((
        (api.colors.lime, api.colors.green),
        (api.colors.yellow, api.colors.brown),
        (api.colors.red, api.colors.orange),
    ), start=1):
        assert await m.setTextColor(tc) is None
        assert await m.getTextColor() == tc
        assert await m.setBackgroundColor(bc) is None
        assert await m.getBackgroundColor() == bc
        assert await m.setCursorPos(offs, offs) is None
        assert await m.getCursorPos() == (offs, offs)
        assert await m.write('text') is None
    assert await m.setBackgroundColor(api.colors.black) is None
    await asyncio.sleep(1)
    for i in range(2):
        assert await m.scroll(-1) is None
        await asyncio.sleep(0.5)
    for i in range(2):
        assert await m.scroll(1) is None
        await asyncio.sleep(0.5)

    await step(api, 'You must have seen three texts with different colors scrolling')

    assert await m.setTextColor(api.colors.white) is None
    assert await m.setBackgroundColor(api.colors.black) is None
    assert await m.clear() is None
    for i in range(1, 5):
        assert await m.setCursorPos(1, i) is None
        assert await m.write((str(i) + '  ') * 4) is None
    await asyncio.sleep(2)
    for i in range(2, 5, 2):
        assert await m.setCursorPos(1, i) is None
        assert await m.clearLine() is None

    await step(api, 'You must have seen some lines disappearing')

    assert await m.setBackgroundColor(api.colors.black) is None
    assert await m.clear() is None
    assert await m.setCursorPos(1, 1) is None
    assert await m.blit(
        'rainbow',
        'e14d3ba',
        'fffffff',
    ) is None
    assert await m.setCursorPos(1, 2) is None
    assert await m.blit(
        'rainbow',
        '0000000',
        'e14d3ba',
    ) is None

    await step(api, 'You must have seen per-letter colored text')

    assert await m.setBackgroundColor(api.colors.black) is None
    assert await m.setTextColor(api.colors.white) is None
    assert await m.getTextScale() == 1
    assert await m.setTextScale(5) is None
    assert await m.getTextScale() == 5
    assert await m.setCursorPos(1, 1) is None
    assert await m.clear() is None
    assert await m.getSize() == (1, 1)
    assert await m.write('AAA') is None

    await step(api, 'You must have seen single large letter A')

    assert await m.setTextScale(1) is None
    assert await m.setBackgroundColor(api.colors.white) is None
    assert await m.clear() is None
    for i, color in enumerate(api.colors):
        await m.setPaletteColor(color, i / 15, 0, 0)
    assert await m.setCursorPos(1, 1) is None
    assert await m.blit(
        ' redtex',
        '0123456',
        '0000000',
    ) is None
    assert await m.setCursorPos(1, 2) is None
    assert await m.blit(
        'tappear',
        '789abcd',
        '0000000',
    ) is None
    assert await m.setCursorPos(1, 3) is None
    assert await m.blit(
        's!',
        'ef',
        '00',
    ) is None

    await step(api, 'You must have seen different shades of red made using palettes')

    await api.print('Remove monitor')
    await api.print('Test finished successfully')


async def test_computer_peripheral(api):
    side = 'left'

    await step(
        api,
        f'Place another computer on {side} side of computer\n'
        "Don't turn it on!",
    )

    c = await api.peripheral.wrap(side)
    assert c is not None

    from computercraft.subapis.peripheral import CCComputer

    tbl = await get_object_table(api, f'peripheral.wrap("{side}")')
    assert get_class_table(CCComputer) == tbl

    assert await c.isOn() is False
    assert isinstance(await c.getID(), int)
    assert await c.getLabel() is None
    assert await c.turnOn() is None

    await step(api, 'Computer must be turned on now')

    assert await c.shutdown() is None

    await step(api, 'Computer must shutdown')

    await step(api, 'Now turn on computer manually and enter some commands')

    assert await c.reboot() is None

    await step(api, 'Computer must reboot')

    await api.print('Test finished successfully')


async def modem_server(api):
    side = 'back'
    m = await api.peripheral.wrap(side)
    listen_channel = 5
    async with m.receive(listen_channel) as q:
        async for msg in q:
            await api.print(repr(msg))
            if msg.content == 'stop':
                break
            else:
                await m.transmit(msg.reply_channel, listen_channel, msg.content)


async def test_modem_peripheral(api):
    # do this test twice: for wired and wireless modems

    side = 'back'

    await step(
        api,
        f'Attach modem to {side} side of computer\n'
        f'Place another computer with similar modem at {side} side\n'
        'In case of wired modems connect them\n'
        'On another computer start py modem_server'
    )

    m = await api.peripheral.wrap(side)

    remote_channel = 5
    local_channel = 7

    assert await m.isOpen(local_channel) is False
    async with m.receive(local_channel) as q:
        assert await m.isOpen(local_channel) is True
        await m.transmit(remote_channel, local_channel, 1)
        await m.transmit(remote_channel, local_channel, 'hi')
        await m.transmit(remote_channel, local_channel, {'data': 5})
        await m.transmit(remote_channel, local_channel, 'stop')

        messages = []
        async for msg in q:
            assert msg.reply_channel == remote_channel
            assert msg.distance > 0
            messages.append(msg.content)
            if len(messages) == 3:
                break

    assert messages == [1, 'hi', {'data': 5}]
    assert await m.isOpen(local_channel) is False
    assert await m.closeAll() is None
    assert isinstance(await m.isWireless(), bool)

    await api.print('Test finished successfully')


async def test_printer_peripheral(api):
    side = 'left'

    await step(api, f'Attach empty printer at {side} side of computer')

    m = await api.peripheral.wrap(side)

    from computercraft.subapis.peripheral import CCPrinter
    tbl = await get_object_table(api, f'peripheral.wrap("{side}")')
    assert get_class_table(CCPrinter) == tbl

    assert await m.getPaperLevel() == 0
    assert await m.getInkLevel() == 0

    # no paper
    assert await m.newPage() is False
    # page not started
    with assert_raises(LuaException):
        await m.endPage()
    with assert_raises(LuaException):
        await m.write('test')
    with assert_raises(LuaException):
        await m.setCursorPos(2, 2)
    with assert_raises(LuaException):
        await m.getCursorPos()
    with assert_raises(LuaException):
        await m.getPageSize()
    with assert_raises(LuaException):
        await m.setPageTitle('title')

    await step(api, 'Put paper into printer')
    paper_level = await m.getPaperLevel()
    assert paper_level > 0
    # no ink
    assert await m.newPage() is False

    await step(api, 'Put ink into printer')
    ink_level = await m.getInkLevel()
    assert ink_level > 0

    assert await m.newPage() is True
    assert await m.getPaperLevel() < paper_level
    assert await m.getInkLevel() < ink_level

    assert await m.setCursorPos(2, 2) is None
    assert await m.getCursorPos() == (2, 2)
    assert await m.setCursorPos(1, 1) is None
    assert await m.getCursorPos() == (1, 1)
    assert await m.setPageTitle('Green bottles') is None
    assert await m.getPageSize() == (25, 21)

    async def row(n=1):
        _, r = await m.getCursorPos()
        await m.setCursorPos(1, r + n)

    def split_text(text, max_width=25):
        for i in range(0, len(text), max_width):
            yield text[i:i + max_width]

    def split_by_words(text, max_width=25):
        stack = []
        stack_len = 0
        for word in text.split(' '):
            assert len(word) <= max_width
            with_word = len(word) if stack_len == 0 else stack_len + 1 + len(word)
            if with_word > max_width:
                yield ' '.join(stack)
                stack.clear()
                stack_len = 0
            else:
                stack.append(word)
                stack_len = with_word
        if stack:
            yield ' '.join(stack)

    async def multiline_write(text):
        _, r = await m.getCursorPos()
        for pt in split_by_words(text):
            assert await m.setCursorPos(1, r) is None
            assert await m.write(pt) is None
            r += 1
        assert await m.setCursorPos(1, r) is None

    assert await m.write('Green bottles'.center(25)) is None
    await row(2)

    x = 2
    while x > 0:
        await multiline_write(f'{x} green bottles hanging on the wall')
        await multiline_write(f'{x} green bottles hanging on the wall')
        await multiline_write('if one green bottle accidently falls')
        x -= 1
        await multiline_write(f'there will be {x} hanging on the wall')
        await row()

    assert await m.endPage() is True

    await api.print('Test finished successfully')


async def test_speaker_peripheral(api):
    side = 'left'

    await step(api, f'Attach speaker at {side} side of computer')

    m = await api.peripheral.wrap(side)

    from computercraft.subapis.peripheral import CCSpeaker
    tbl = await get_object_table(api, f'peripheral.wrap("{side}")')
    assert get_class_table(CCSpeaker) == tbl

    for _ in range(48):
        assert await m.playNote(
            random.choice([
                'bass', 'basedrum', 'bell', 'chime', 'flute', 'guitar', 'hat',
                'snare', 'xylophone', 'iron_xylophone', 'pling', 'banjo',
                'bit', 'didgeridoo', 'cow_bell',
            ]),
            3,
            random.randint(0, 24)
        ) is True
        await asyncio.sleep(0.2)

    assert await m.playSound('minecraft:entity.player.levelup') is True

    await api.print('You must have heard notes and sounds')
    await api.print('Test finished successfully')


async def test_commandblock_peripheral(api):
    side = 'left'

    await step(api, f'Attach command block at {side} side of computer')

    m = await api.peripheral.wrap(side)

    from computercraft.subapis.peripheral import CCCommandBlock
    tbl = await get_object_table(api, f'peripheral.wrap("{side}")')
    assert get_class_table(CCCommandBlock) == tbl

    assert await m.getCommand() == ''
    assert await m.setCommand('say Hello from python side') is None
    assert await m.getCommand() == 'say Hello from python side'
    assert await m.runCommand() is None

    assert await m.setCommand('time query daytime') is None
    assert await m.getCommand() == 'time query daytime'
    assert await m.runCommand() is None

    assert await m.setCommand('') is None
    assert await m.getCommand() == ''
    with assert_raises(LuaException):
        await m.runCommand()

    await api.print('You must have seen chat message')
    await api.print('Test finished successfully')


async def test_modem_wrap(api):
    side = 'back'

    await step(api, f'Attach and disable (right-click) wired modem at {side} side')

    m = await api.peripheral.wrap(side)
    assert await m.isWireless() is False
    assert await m.getNameLocal() is None

    await step(api, f'Enable (right-click) wired modem at {side} side')

    assert isinstance(await m.getNameLocal(), str)

    await step(api, 'Connect networked speaker peripheral & enable its modem')

    names = await m.getNamesRemote()
    assert isinstance(names, list)
    assert len(names) > 0
    speaker = []
    for n in names:
        assert isinstance(n, str)
        if n.startswith('speaker_'):
            speaker.append(n)
    assert len(speaker) == 1
    speaker = speaker[0]

    assert await m.isPresentRemote('doesnotexist') is False
    assert await m.getTypeRemote('doesnotexist') is None

    assert await m.isPresentRemote(speaker) is True
    assert await m.getTypeRemote(speaker) == 'speaker'

    assert await m.wrapRemote('doesnotexist') is None
    s = await m.wrapRemote(speaker)

    assert await s.playSound('minecraft:entity.player.levelup') is True

    await api.print('You must have heard levelup sound')
    await api.print('Test finished successfully')


async def test_turtle_peripheral(api):
    raise NotImplementedError


async def test_textutils(api):
    assert await api.textutils.slowWrite('write ') is None
    assert await api.textutils.slowWrite('write ', 5) is None
    assert await api.textutils.slowPrint('print') is None
    assert await api.textutils.slowPrint('print', 5) is None

    assert await api.textutils.formatTime(0) == '0:00 AM'
    assert await api.textutils.formatTime(0, True) == '0:00'

    table = [
        api.colors.red,
        ['Planet', 'Distance', 'Mass'],
        api.colors.gray,
        ['Mercury', '0.387', '0.055'],
        api.colors.lightGray,
        ['Venus', '0.723', '0.815'],
        api.colors.green,
        ['Earth', '1.000', '1.000'],
        api.colors.red,
        ['Mars', '1.524', '0.107'],
        api.colors.orange,
        ['Jupiter', '5.203', '318'],
        api.colors.yellow,
        ['Saturn', '9.537', '95'],
        api.colors.cyan,
        ['Uranus', '19.191', '14.5'],
        api.colors.blue,
        ['Neptune', '30.069', '17'],
        api.colors.white,
    ]

    assert await api.textutils.tabulate(*table) is None

    lines = await api.textutils.pagedPrint('''
Lorem ipsum dolor sit amet, consectetur adipiscing elit.
Suspendisse feugiat diam et velit aliquam, nec porttitor eros facilisis.
Nulla facilisi.
Sed eget dui vel tellus aliquam fermentum.
Aliquam sed lorem congue, dignissim nulla in, porta diam.
Aliquam erat volutpat.
    '''.strip())
    assert isinstance(lines, int)
    assert lines > 0

    assert await api.textutils.pagedTabulate(*table[:-1], *table[2:-1], *table[2:]) is None

    assert api.textutils.complete('co', ['command', 'row', 'column']) == [
        'mmand', 'lumn']

    await api.print('Test finished successfully')


async def test_pocket(api):
    assert await api.peripheral.isPresent('back') is False

    from computercraft.subapis.pocket import PocketAPI
    tbl = await get_object_table(api, 'pocket')
    assert get_class_table(PocketAPI) == tbl

    await step(api, 'Clean inventory from any pocket upgrades')

    with assert_raises(LuaException):
        await api.pocket.equipBack()
    with assert_raises(LuaException):
        await api.pocket.unequipBack()
    assert await api.peripheral.isPresent('back') is False

    await step(api, 'Put any pocket upgrade to inventory')

    assert await api.pocket.equipBack() is None
    assert await api.peripheral.isPresent('back') is True

    assert await api.pocket.unequipBack() is None
    assert await api.peripheral.isPresent('back') is False

    await api.print('Test finished successfully')


async def test_multishell(api):
    from computercraft.subapis.multishell import MultishellAPI
    tbl = await get_object_table(api, 'multishell')
    assert get_class_table(MultishellAPI) == tbl

    await step(api, 'Close all additional shells')

    assert await api.multishell.getCount() == 1
    assert await api.multishell.getCurrent() == 1
    assert await api.multishell.getFocus() == 1
    assert isinstance(await api.multishell.getTitle(1), str)

    title = f'new title {random.randint(1, 1000000)}'
    assert await api.multishell.setTitle(1, title) is None
    assert await api.multishell.getTitle(1) == title

    assert await api.multishell.setFocus(1) is True
    assert await api.multishell.setFocus(0) is False
    assert await api.multishell.setFocus(2) is False

    assert await api.multishell.getTitle(2) is None

    assert await api.multishell.launch({}, 'rom/programs/fun/hello.lua') == 2
    assert isinstance(await api.multishell.getTitle(2), str)

    await api.print('Test finished successfully')


async def test_shell(api):
    from computercraft.subapis.shell import ShellAPI
    tbl = await get_object_table(api, 'shell')

    del tbl['function']['setCompletionFunction']
    del tbl['function']['getCompletionInfo']
    assert get_class_table(ShellAPI) == tbl

    assert await api.shell.complete('ls ro') == ['m/', 'm']
    assert await api.shell.completeProgram('lu') == ['a']

    ps = await api.shell.programs()
    assert 'shutdown' in ps

    als = await api.shell.aliases()
    assert 'ls' in als
    assert als['ls'] == 'list'
    assert 'xls' not in als
    assert await api.shell.setAlias('xls', 'list') is None
    als = await api.shell.aliases()
    assert 'xls' in als
    assert als['xls'] == 'list'
    assert await api.shell.clearAlias('xls') is None
    als = await api.shell.aliases()
    assert 'xls' not in als

    assert await api.shell.getRunningProgram() == 'py'

    assert await api.shell.resolveProgram('doesnotexist') is None
    assert await api.shell.resolveProgram('hello') == 'rom/programs/fun/hello.lua'

    assert await api.shell.dir() == ''
    assert await api.shell.resolve('doesnotexist') == 'doesnotexist'
    assert await api.shell.resolve('startup.lua') == 'startup.lua'
    assert await api.shell.setDir('rom') is None
    assert await api.shell.dir() == 'rom'
    assert await api.shell.resolve('startup.lua') == 'rom/startup.lua'
    assert await api.shell.setDir('') is None

    assert isinstance(await api.shell.path(), str)
    assert await api.shell.setPath(await api.shell.path()) is None

    assert await api.shell.execute('hello') is True
    assert await api.shell.run('hello') is True
    assert await api.shell.execute('doesnotexist') is False
    assert await api.shell.run('doesnotexist') is False

    tab = await api.shell.openTab('hello')
    assert isinstance(tab, int)

    await step(api, f'Program has been launched in tab {tab}')

    assert await api.shell.switchTab(tab) is None

    await step(api, 'Computer will shutdown after test due to shell.exit')

    assert await api.shell.exit() is None

    await api.print('Test finished successfully')


async def test_window(api):
    async with api.window.create(
        api.term.get_current_target(),
        15, 5, 5, 5, False,
    ) as win:
        assert await win.getPosition() == (15, 5)
        assert await win.getSize() == (5, 5)

        await win.setBackgroundColor(api.colors.red)
        await win.clear()
        await win.setVisible(True)

        await asyncio.sleep(1)

        await win.setVisible(False)
        await win.setCursorPos(1, 1)
        await win.setTextColor(api.colors.yellow)
        await win.write('*********')
        await win.setVisible(True)

        await asyncio.sleep(1)

        await api.term.clear()

        await asyncio.sleep(1)

        await win.redraw()
        assert await win.getLine(1) == ('*****', '44444', 'eeeee')

        # draws immediately
        await win.reposition(21, 5)
        await win.reposition(27, 5)

    await api.print('Test finished successfully')


async def test_redirect_to_window(api):
    w, h = await api.term.getSize()
    async with AsyncExitStack() as stack:
        left = await stack.enter_async_context(api.window.create(
            api.term.get_current_target(),
            1, 1, w // 2, h, True,
        ))
        right = await stack.enter_async_context(api.window.create(
            api.term.get_current_target(),
            w // 2 + 1, 1, w // 2, h, True,
        ))
        async with api.term.redirect(left.get_term_target()):
            await api.term.setBackgroundColor(api.colors.green)
            await api.term.setTextColor(api.colors.white)
            await api.term.clear()
            await api.term.setCursorPos(1, h // 2)
            await api.print('Left part')
        async with api.term.redirect(right.get_term_target()):
            await api.term.setBackgroundColor(api.colors.red)
            await api.term.setTextColor(api.colors.yellow)
            await api.term.clear()
            await api.term.setCursorPos(1, h // 2)
            await api.print('Right part')
        await api.print('Default terminal restored')

    await api.print('Test finished successfully')


async def test_redirect_to_local_monitor(api):
    side = 'left'
    await step(api, f'Attach 3x3 color monitor to {side} side of computer')

    async with api.term.redirect(api.peripheral.get_term_target(side)):
        await api.term.setBackgroundColor(api.colors.green)
        await api.term.setTextColor(api.colors.white)
        await api.term.clear()
        await api.term.setCursorPos(1, 1)
        await api.print('Redirected to monitor')

    await api.print('Test finished successfully')


async def test_redirect_to_remote_monitor(api):
    side = 'back'
    await step(api, f'Attach wired modem to {side} side of computer')

    mod = await api.peripheral.wrap(side)

    await step(api, 'Connect remote monitor using wires, activate its modem')

    for name in await mod.getNamesRemote():
        if await mod.getTypeRemote(name) == 'monitor':
            break
    else:
        assert False

    async with api.term.redirect(api.peripheral.get_term_target(name)):
        await api.term.setBackgroundColor(api.colors.blue)
        await api.term.setTextColor(api.colors.white)
        await api.term.clear()
        await api.term.setCursorPos(1, 1)
        await api.print('Redirected to monitor')

    await api.print('Test finished successfully')


pixels = '''
0000000030030033333333330000000003000000000000000
0333300000000033333333300000000000333333000000330
0803000000803033333333000000000000880330300003000
0800800030330333333333000300883000888880000033000
3333000000003333333333300080038880000080000888003
33333ddd3333333333333333300000333330000000000d033
333dddddd3333333333333333333333333333333333ddd333
3333ccdd333333333333344444444333333333333dddddd33
333cc33d3333333333334444444444333333333335d3cc33d
5ddc33333333333333344444444444433333333333333cd55
dddc555d3333333333344444444444433333333333d5dc5dd
d5dd5dd4bbbbbbbbb999b00b00300b3bb9999bbbb4ddddddd
ddd55444bb999993bbb33390b030bb9999bbbbbbb444ddddd
55dd44bbbbbbbbbbbbb9bb3003003bbb339bbbbbbbb44444d
dd444bbbbbbbbbbb99933bbb0030b999bbbbbbbbbbbbbbb44
444bbbbbbbbbbbbbbb9bbb33b309933bbbbbbbbbbbbbbbbbb
bbbbbbbbbbbbbbbbbbbb9bbbb3bbbb99bbbbbbbbbbbbbbbbb
bbbbbbbbbbbbbbbbbbbbbb399399bbbbbbbbbbbbbbbbbbbbb
'''.strip()


async def test_paintutils(api):
    from computercraft.subapis.paintutils import PaintutilsAPI
    tbl = await get_object_table(api, 'paintutils')
    assert get_class_table(PaintutilsAPI) == tbl

    async with api.fs.open('img.nfp', 'w') as f:
        await f.write(pixels)

    # from pprint import pprint
    int_pixels = await api.paintutils.loadImage('img.nfp')
    assert len(int_pixels) > 0
    assert len(int_pixels[0]) > 0
    assert await api.paintutils.parseImage(pixels) == int_pixels

    assert await api.paintutils.drawImage(int_pixels, 1, 1) is None

    await asyncio.sleep(2)

    await api.term.setTextColor(api.colors.white)
    await api.term.setBackgroundColor(api.colors.black)
    await api.term.clear()
    await api.term.setBackgroundColor(api.colors.green)

    by = 3
    bx = 3

    assert await api.paintutils.drawPixel(bx, by) is None
    assert await api.paintutils.drawPixel(bx + 1, by, api.colors.red) is None

    bx += 5

    assert await api.paintutils.drawLine(bx, by, bx + 3, by + 3) is None
    assert await api.paintutils.drawLine(bx + 3, by, bx, by + 3, api.colors.red) is None

    bx += 5
    assert await api.paintutils.drawBox(bx, by, bx + 3, by + 3) is None
    bx += 5
    assert await api.paintutils.drawBox(bx, by, bx + 3, by + 3, api.colors.red) is None

    bx += 5
    assert await api.paintutils.drawFilledBox(bx, by, bx + 3, by + 3) is None
    bx += 5
    assert await api.paintutils.drawFilledBox(bx, by, bx + 3, by + 3, api.colors.red) is None

    await api.term.setCursorPos(1, by + 6)

    await asyncio.sleep(2)

    await api.print('Test finished successfully')


async def test_rednet(api):
    from computercraft.subapis.rednet import RednetAPI
    tbl = await get_object_table(api, 'rednet')
    del tbl['function']['run']
    assert get_class_table(RednetAPI) == tbl

    side = 'back'

    await step(api, f'Attach modem to {side} side of computer')

    assert await api.rednet.isOpen(side) is False
    assert await api.rednet.isOpen() is False

    with assert_raises(LuaException):
        await api.rednet.close('doesnotexist')

    assert await api.rednet.close(side) is None

    with assert_raises(LuaException):
        await api.rednet.open('doesnotexist')

    assert await api.rednet.open(side) is None
    assert await api.rednet.isOpen(side) is True

    with assert_raises(LuaException):
        # disallowed hostname
        await api.rednet.host('helloproto', 'localhost')
    assert await api.rednet.host('helloproto', 'alpha') is None

    cid = await api.os.getComputerID()

    assert await api.rednet.lookup('helloproto', 'localhost') == cid
    assert await api.rednet.lookup('helloproto') == [cid]
    assert await api.rednet.lookup('nonexistent', 'localhost') is None
    assert await api.rednet.lookup('nonexistent') == []

    assert await api.rednet.unhost('helloproto') is None

    assert await api.rednet.send(cid + 100, 'message', 'anyproto') is True
    assert await api.rednet.broadcast('message', 'anyproto') is None

    assert await api.rednet.receive(timeout=1) is None
    assert await asyncio.gather(
        api.rednet.receive(timeout=1),
        api.rednet.send(cid, 'message'),
    ) == [(cid, 'message', None), True]

    assert await api.rednet.close() is None
    assert await api.rednet.isOpen(side) is False

    await api.print('Test finished successfully')


async def test_turtle(api):
    from computercraft.subapis.turtle import TurtleAPI
    tbl = await get_object_table(api, 'turtle')
    assert tbl['table'] == {'native': True}
    del tbl['table']
    tbl['function'].setdefault('craft', True)
    assert get_class_table(TurtleAPI) == tbl

    flimit = await api.turtle.getFuelLimit()
    assert isinstance(flimit, int)
    assert flimit > 0

    flevel = await api.turtle.getFuelLevel()
    assert isinstance(flevel, int)
    assert 0 <= flevel <= flimit

    assert await api.turtle.select(2) is None
    assert await api.turtle.getSelectedSlot() == 2
    with assert_raises(LuaException):
        await api.turtle.select(0)
    assert await api.turtle.select(1) is None
    assert await api.turtle.getSelectedSlot() == 1

    await step(api, 'Put 3 coals into slot 1')

    assert await api.turtle.getItemCount() == 3
    assert await api.turtle.getItemCount(1) == 3

    assert await api.turtle.getItemDetail() == {
        'count': 3,
        'name': 'minecraft:coal',
    }
    assert await api.turtle.getItemDetail(1) == {
        'count': 3,
        'name': 'minecraft:coal',
    }

    assert await api.turtle.getItemSpace() == 61
    assert await api.turtle.getItemSpace(1) == 61

    assert await api.turtle.refuel(1) is None

    assert await api.turtle.getFuelLevel() > flevel
    flevel = await api.turtle.getFuelLevel()
    assert await api.turtle.getItemCount() == 2

    assert await api.turtle.refuel() is None

    assert await api.turtle.getFuelLevel() > flevel
    assert await api.turtle.getItemCount() == 0

    with assert_raises(LuaException):
        await api.turtle.refuel(1)
    with assert_raises(LuaException):
        await api.turtle.refuel()

    await step(api, 'Remove blocks in front/below/above turtle')

    assert await api.turtle.detect() is False
    assert await api.turtle.detectUp() is False
    assert await api.turtle.detectDown() is False

    assert await api.turtle.inspect() is None
    assert await api.turtle.inspectUp() is None
    assert await api.turtle.inspectDown() is None

    await step(api, 'Put cobblestone blocks in front/below/above turtle')

    assert await api.turtle.detect() is True
    assert await api.turtle.detectUp() is True
    assert await api.turtle.detectDown() is True

    for c in [
        await api.turtle.inspect(),
        await api.turtle.inspectUp(),
        await api.turtle.inspectDown()
    ]:
        assert isinstance(c, dict)
        assert c['name'] == 'minecraft:cobblestone'

    assert await api.turtle.select(1) is None
    assert await api.turtle.getItemCount() == 0
    assert await api.turtle.equipLeft() is None

    assert await api.turtle.select(2) is None
    assert await api.turtle.getItemCount() == 0
    assert await api.turtle.equipRight() is None

    if (
        await api.turtle.getItemCount(1) != 0
        or await api.turtle.getItemCount(2) != 0
    ):
        await step(api, 'Remove all items from slots 1 and 2')

    assert await api.turtle.select(1) is None
    if await api.turtle.getItemDetail(1) != {
        'count': 1,
        'name': 'minecraft:diamond_pickaxe',
    }:
        await step(api, 'Put fresh diamond pickaxe at slot 1')

    assert await api.turtle.equipLeft() is None

    assert await api.turtle.dig() is True
    assert await api.turtle.dig() is False
    assert await api.turtle.digUp() is True
    assert await api.turtle.digUp() is False
    assert await api.turtle.digDown() is True
    assert await api.turtle.digDown() is False

    assert await api.turtle.getItemCount() == 3

    assert await api.turtle.forward() is True
    assert await api.turtle.back() is True
    assert await api.turtle.up() is True
    assert await api.turtle.down() is True
    assert await api.turtle.turnLeft() is None
    assert await api.turtle.turnRight() is None

    assert await api.turtle.place() is True
    assert await api.turtle.place() is False
    assert await api.turtle.placeUp() is True
    assert await api.turtle.placeUp() is False
    assert await api.turtle.placeDown() is True
    with assert_raises(LuaException, 'No items to place'):
        await api.turtle.placeDown()

    await step(api, 'Put 3 cobblestone blocks to slot 1')

    assert await api.turtle.getItemCount(1) == 3
    assert await api.turtle.getItemCount(2) == 0

    assert await api.turtle.compare() is True
    assert await api.turtle.compareUp() is True
    assert await api.turtle.compareDown() is True

    assert await api.turtle.select(2) is None

    assert await api.turtle.compare() is False
    assert await api.turtle.compareUp() is False
    assert await api.turtle.compareDown() is False

    assert await api.turtle.select(1) is None

    assert await api.turtle.transferTo(2, 1) is True
    assert await api.turtle.getItemCount(1) == 2
    assert await api.turtle.getItemCount(2) == 1
    assert await api.turtle.compareTo(2) is True

    assert await api.turtle.transferTo(2) is True
    assert await api.turtle.getItemCount(1) == 0
    assert await api.turtle.getItemCount(2) == 3
    assert await api.turtle.compareTo(2) is False

    assert await api.turtle.select(2) is None
    assert await api.turtle.transferTo(1) is True
    assert await api.turtle.select(1) is None
    assert await api.turtle.dig() is True
    assert await api.turtle.digUp() is True
    assert await api.turtle.digDown() is True
    assert await api.turtle.getItemCount() == 6

    assert await api.turtle.drop(1) is True
    assert await api.turtle.dropUp(1) is True
    assert await api.turtle.dropDown(1) is True
    assert await api.turtle.getItemCount() == 3
    assert await api.turtle.drop() is True
    assert await api.turtle.getItemCount() == 0
    assert await api.turtle.drop() is False

    await step(
        api,
        'Collect dropped cobblestone\n'
        'Drop stack of sticks right in front of the turtle\n'
        'Its better to build 1-block room then throw sticks there',
    )

    assert await api.turtle.suck(1) is True
    assert await api.turtle.getItemCount() == 1
    assert await api.turtle.suck() is True
    assert await api.turtle.getItemCount() == 64
    assert await api.turtle.suck() is False
    assert await api.turtle.drop() is True
    assert await api.turtle.getItemCount() == 0

    await step(
        api,
        'Collect dropped sticks\n'
        'Drop stack of sticks right below the turtle\n'
        'Its better to build 1-block room then throw sticks there',
    )

    assert await api.turtle.suckDown(1) is True
    assert await api.turtle.getItemCount() == 1
    assert await api.turtle.suckDown() is True
    assert await api.turtle.getItemCount() == 64
    assert await api.turtle.suckDown() is False
    assert await api.turtle.dropDown() is True
    assert await api.turtle.getItemCount() == 0

    await step(
        api,
        'Collect dropped sticks\n'
        'Drop stack of sticks right above the turtle\n'
        'Its better to build 1-block room then throw sticks there',
    )

    assert await api.turtle.suckUp(1) is True
    assert await api.turtle.getItemCount() == 1
    assert await api.turtle.suckUp() is True
    assert await api.turtle.getItemCount() == 64
    assert await api.turtle.suckUp() is False
    assert await api.turtle.dropUp() is True
    assert await api.turtle.getItemCount() == 0

    async def craft1():
        return await api.turtle.craft()

    async def craft2():
        c = await api.peripheral.wrap('right')
        return await c.craft()

    await step(api, 'Put crafting table into slot 1')
    assert await api.turtle.select(1) is None
    assert await api.turtle.equipRight() is None

    for craft_fn in craft1, craft2:
        await step(
            api,
            'Clean inventory of turtle\n'
            'Put 8 cobblestones into slot 1',
        )

        assert await api.turtle.select(1) is None
        assert await craft_fn() is False
        for idx in [2, 3, 5, 7, 9, 10, 11]:
            assert await api.turtle.transferTo(idx, 1)
        assert await craft_fn() is True
        assert await craft_fn() is False
        assert await api.turtle.getItemDetail() == {
            'count': 1,
            'name': 'minecraft:furnace',
        }

    await api.print('Test finished successfully')


async def test_turtle_attack(api):
    await step(
        api,
        'NOTE: this test is unreliable\n'
        'Build 1x1x1 stone cage in front of turtle\n'
        'Spawn here a chicken',
    )

    assert await api.turtle.attack() is True
    assert await api.turtle.attack() is True
    assert await api.turtle.attack() is False

    await step(
        api,
        'Build 1x1x1 stone cage below turtle\n'
        'Spawn here a chicken',
    )

    assert await api.turtle.attackDown() is True
    assert await api.turtle.attackDown() is True
    assert await api.turtle.attackDown() is False

    await step(
        api,
        'Build 1x1x1 stone cage above turtle\n'
        'Spawn here a chicken',
    )

    assert await api.turtle.attackUp() is True
    assert await api.turtle.attackUp() is True
    assert await api.turtle.attackUp() is False

    await api.print('Test finished successfully')


# vector won't be implemented, use python equivalent
