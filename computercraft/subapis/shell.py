from typing import List, Dict, Optional

from .. import ser
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
    return method('setDir', ser.encode(path)).take_none()


def path() -> str:
    return method('path').take_string()


def setPath(path: str):
    return method('setPath', ser.encode(path)).take_none()


def resolve(localPath: str) -> str:
    return method('resolve', ser.encode(localPath)).take_string()


def resolveProgram(name: str) -> Optional[str]:
    return method('resolveProgram', ser.encode(name)).take_option_string()


def aliases() -> Dict[str, str]:
    d = method('aliases').take_dict()
    return {ser.decode(k): ser.decode(v) for k, v in d.items()}


def setAlias(alias: str, program: str):
    return method('setAlias', ser.encode(alias), ser.encode(program)).take_none()


def clearAlias(alias: str):
    return method('clearAlias', ser.encode(alias)).take_none()


def programs(showHidden: bool = None) -> List[str]:
    return method('programs', showHidden).take_list_of_strings()


def getRunningProgram() -> str:
    return method('getRunningProgram').take_string()


def run(command: str, *args: str) -> bool:
    args = tuple(ser.encode(a) for a in args)
    return method('run', ser.encode(command), *args).take_bool()


def execute(command: str, *args: str) -> bool:
    args = tuple(ser.encode(a) for a in args)
    return method('execute', ser.encode(command), *args).take_bool()


def openTab(command: str, *args: str) -> int:
    args = tuple(ser.encode(a) for a in args)
    return method('openTab', ser.encode(command), *args).take_int()


def switchTab(tabID: int):
    return method('switchTab', tabID).take_none()


def complete(prefix: str) -> List[str]:
    return method('complete', ser.encode(prefix)).take_list_of_strings()


def completeProgram(prefix: str) -> List[str]:
    return method('completeProgram', ser.encode(prefix)).take_list_of_strings()

# TODO: ?
# these functions won't be implemented
# it's far better to keep this in lua code

# setCompletionFunction
# getCompletionInfo

# we can create callbacks to python code, but this will require
# connection to python, and will break the shell if python disconnects
