from typing import List, Dict, Optional

from ..sess import eval_lua_method_factory


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


def exit():
    return method('exit').take_none()


def dir() -> str:
    return method('dir').take_string()


def setDir(path: str):
    return method('setDir', path).take_none()


def path() -> str:
    return method('path').take_string()


def setPath(path: str):
    return method('setPath', path).take_none()


def resolve(localPath: str) -> str:
    return method('resolve', localPath).take_string()


def resolveProgram(name: str) -> Optional[str]:
    return method('resolveProgram', name).take_option_string()


def aliases() -> Dict[str, str]:
    d = method('aliases').take_dict()
    return {k.decode('latin1'): v.decode('latin1') for k, v in d.items()}


def setAlias(alias: str, program: str):
    return method('setAlias', alias, program).take_none()


def clearAlias(alias: str):
    return method('clearAlias', alias).take_none()


def programs(showHidden: bool = None) -> List[str]:
    return method('programs', showHidden).take_list_of_strings()


def getRunningProgram() -> str:
    return method('getRunningProgram').take_string()


def run(command: str, *args: str) -> bool:
    return method('run', command, *args).take_bool()


def execute(command: str, *args: str) -> bool:
    return method('execute', command, *args).take_bool()


def openTab(command: str, *args: str) -> int:
    return method('openTab', command, *args).take_int()


def switchTab(tabID: int):
    return method('switchTab', tabID).take_none()


def complete(prefix: str) -> List[str]:
    return method('complete', prefix).take_list_of_strings()


def completeProgram(prefix: str) -> List[str]:
    return method('completeProgram', prefix).take_list_of_strings()

# TODO: ?
# these functions won't be implemented
# it's far better to keep this in lua code

# setCompletionFunction
# getCompletionInfo

# we can create callbacks to python code, but this will require
# connection to python, and will break the shell if python disconnects
