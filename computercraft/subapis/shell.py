from typing import List, Dict, Optional

from ..sess import eval_lua


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


def exit() -> None:
    return eval_lua(b'G:shell:M:exit').take_none()


def dir() -> str:
    return eval_lua(b'G:shell:M:dir').take_string()


def setDir(path: str) -> None:
    return eval_lua(b'G:shell:M:setDir', path).take_none()


def path() -> str:
    return eval_lua(b'G:shell:M:path').take_string()


def setPath(path: str) -> None:
    return eval_lua(b'G:shell:M:setPath', path).take_none()


def resolve(localPath: str) -> str:
    return eval_lua(b'G:shell:M:resolve', localPath).take_string()


def resolveProgram(name: str) -> Optional[str]:
    return eval_lua(b'G:shell:M:resolveProgram', name).take_option_string()


def aliases() -> Dict[str, str]:
    return eval_lua(b'G:shell:M:aliases').take_dict()


def setAlias(alias: str, program: str) -> None:
    return eval_lua(b'G:shell:M:setAlias', alias, program).take_none()


def clearAlias(alias: str) -> None:
    return eval_lua(b'G:shell:M:clearAlias', alias).take_none()


def programs(showHidden: bool = None) -> List[str]:
    return eval_lua(b'G:shell:M:programs', showHidden).take_list_of_strings()


def getRunningProgram() -> str:
    return eval_lua(b'G:shell:M:getRunningProgram').take_string()


def run(command: str, *args: str) -> bool:
    return eval_lua(b'G:shell:M:run', command, *args).take_bool()


def execute(command: str, *args: str) -> bool:
    return eval_lua(b'G:shell:M:execute', command, *args).take_bool()


def openTab(command: str, *args: str) -> int:
    return eval_lua(b'G:shell:M:openTab', command, *args).take_int()


def switchTab(tabID: int) -> None:
    return eval_lua(b'G:shell:M:switchTab', tabID).take_none()


def complete(prefix: str) -> List[str]:
    return eval_lua(b'G:shell:M:complete', prefix).take_list_of_strings()


def completeProgram(prefix: str) -> List[str]:
    return eval_lua(b'G:shell:M:completeProgram', prefix).take_list_of_strings()

# TODO: ?
# these functions won't be implemented
# it's far better to keep this in lua code

# setCompletionFunction
# getCompletionInfo

# we can create callbacks to python code, but this will require
# connection to python, and will break the shell if python disconnects
