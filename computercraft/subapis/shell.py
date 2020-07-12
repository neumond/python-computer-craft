from typing import List, Dict, Optional

from ..rproc import nil, string, boolean, integer, array_string, fact_mono_dict, option_string
from ..sess import eval_lua_method_factory


map_string_string = fact_mono_dict(string, string)
method = eval_lua_method_factory('shell.')


__all__ = (
    'exit',
    'dir',
    'setDir',
    'path',
    'setPath',
    'resolve',
    'resolveProgram',
    'aliases',
    'setAlias',
    'clearAlias',
    'programs',
    'getRunningProgram',
    'run',
    'execute',
    'openTab',
    'switchTab',
    'complete',
    'completeProgram',
)


def exit(self):
    return nil(method('exit'))


def dir(self) -> str:
    return string(method('dir'))


def setDir(path: str):
    return nil(method('setDir', path))


def path(self) -> str:
    return string(method('path'))


def setPath(path: str):
    return nil(method('setPath', path))


def resolve(localPath: str) -> str:
    return string(method('resolve', localPath))


def resolveProgram(name: str) -> Optional[str]:
    return option_string(method('resolveProgram', name))


def aliases(self) -> Dict[str, str]:
    return map_string_string(method('aliases'))


def setAlias(alias: str, program: str):
    return nil(method('setAlias', alias, program))


def clearAlias(alias: str):
    return nil(method('clearAlias', alias))


def programs(showHidden: bool = None) -> List[str]:
    return array_string(method('programs', showHidden))


def getRunningProgram(self) -> str:
    return string(method('getRunningProgram'))


def run(command: str, *args: str) -> bool:
    return boolean(method('run', command, *args))


def execute(command: str, *args: str) -> bool:
    return boolean(method('execute', command, *args))


def openTab(command: str, *args: str) -> int:
    return integer(method('openTab', command, *args))


def switchTab(tabID: int):
    return nil(method('switchTab', tabID))


def complete(prefix: str) -> List[str]:
    return array_string(method('complete', prefix))


def completeProgram(prefix: str) -> List[str]:
    return array_string(method('completeProgram', prefix))

# TODO: ?
# these functions won't be implemented
# it's far better to keep this in lua code

# setCompletionFunction
# getCompletionInfo

# we can create callbacks to python code, but this will require
# connection to python, and will break the shell if python disconnects
