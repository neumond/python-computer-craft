from cc import import_file, shell

_lib = import_file('_lib.py', __file__)


assert shell.complete('ls ro') == ['m/', 'm']
assert shell.completeProgram('lu') == ['a']

ps = shell.programs()
assert 'shutdown' in ps

als = shell.aliases()
assert 'ls' in als
assert als['ls'] == 'list'
assert 'xls' not in als
assert shell.setAlias('xls', 'list') is None
als = shell.aliases()
assert 'xls' in als
assert als['xls'] == 'list'
assert shell.clearAlias('xls') is None
als = shell.aliases()
assert 'xls' not in als

assert shell.getRunningProgram() == 'py'

assert shell.resolveProgram('doesnotexist') is None
assert shell.resolveProgram('hello') == 'rom/programs/fun/hello.lua'

assert shell.dir() == ''
assert shell.resolve('doesnotexist') == 'doesnotexist'
assert shell.resolve('startup.lua') == 'startup.lua'
assert shell.setDir('rom') is None
assert shell.dir() == 'rom'
assert shell.resolve('startup.lua') == 'rom/startup.lua'
assert shell.setDir('') is None

assert isinstance(shell.path(), str)
assert shell.setPath(shell.path()) is None

assert shell.execute('hello') is True
assert shell.run('hello') is True
assert shell.execute('doesnotexist') is False
assert shell.run('doesnotexist') is False

tab = shell.openTab('hello')
assert isinstance(tab, int)

_lib.step(f'Program has been launched in tab {tab}')

assert shell.switchTab(tab) is None

_lib.step('Computer will shutdown after test due to shell.exit')

assert shell.exit() is None

print('Test finished successfully')
