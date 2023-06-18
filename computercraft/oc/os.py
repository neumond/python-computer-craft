from typing import NoReturn

from ..sess import eval_lua


__all__ = (
    'clock',
    'date',
    'time',
    'sleep',
    'exit',
    'tmpname',
)


def clock() -> float:
    return eval_lua(b'R:os:M:clock').take_number()


def date() -> str:
    # TODO: add parameters
    return eval_lua(b'R:os:M:date').take_string()


def time() -> float:
    return eval_lua(b'R:os:M:time').take_number()


def sleep(seconds: float) -> None:
    return eval_lua(b'R:os:M:sleep').take_none()


def exit() -> NoReturn:
    # TODO: add exit codes
    raise SystemExit


def tmpname() -> str:
    return eval_lua(b'R:os:M:tmpname').take_string()


# TODO: implement
# os.execute
# os.getenv
# os.setenv
