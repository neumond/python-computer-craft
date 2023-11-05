from typing import Optional

from ..lua import LuaNum
from ..sess import eval_lua
from ..sess import get_current_greenlet


__all__ = (
    'version',
    'getComputerID',
    'getComputerLabel',
    'setComputerLabel',
    'run',
    'captureEvent',
    'queueEvent',
    'clock',
    'time',
    'day',
    'epoch',
    'sleep',
    'startTimer',
    'cancelTimer',
    'setAlarm',
    'cancelAlarm',
    'shutdown',
    'reboot',
)


def version() -> str:
    return eval_lua(b'G:os:M:version').take_string()


def getComputerID() -> int:
    return eval_lua(b'G:os:M:getComputerID').take_int()


def getComputerLabel() -> Optional[str]:
    return eval_lua(b'G:os:M:getComputerLabel').take_option_string()


def setComputerLabel(label: Optional[str]):
    return eval_lua(b'G:os:M:setComputerLabel', label).take_none()


def run(environment: dict, programPath: str, *args: str):
    return eval_lua(b'G:os:M:run', environment, programPath, *args).take_bool()


def captureEvent(event: str):
    glet = get_current_greenlet().cc_greenlet
    sess = glet._sess
    evr = sess._evr
    evr.sub(glet._task_id, event)
    try:
        while True:
            val = evr.get_from_stack(glet._task_id, event)
            if val is None:
                res = sess._server_greenlet.switch()
                assert res == 'event'
            else:
                yield val
    finally:
        evr.unsub(glet._task_id, event)


def queueEvent(event: str, *params):
    return eval_lua(b'G:os:M:queueEvent', event, *params).take_none()


def clock() -> LuaNum:
    # number of game ticks * 0.05, roughly seconds
    return eval_lua(b'G:os:M:clock').take_number()


# regarding ingame parameter below:
# python has great stdlib to deal with real current time
# we keep here only in-game time methods and parameters

def time(locale=b'ingame') -> LuaNum:
    # in hours 0..24
    return eval_lua(b'G:os:M:time', locale).take_number()


def day(locale=b'ingame') -> int:
    return eval_lua(b'G:os:M:day', locale).take_int()


def epoch(locale=b'ingame') -> int:
    return eval_lua(b'G:os:M:epoch', locale).take_int()


def sleep(seconds: LuaNum):
    return eval_lua(b'G:os:M:sleep', seconds).take_none()


def startTimer(timeout: LuaNum) -> int:
    return eval_lua(b'G:os:M:startTimer', timeout).take_int()


def cancelTimer(timerID: int):
    return eval_lua(b'G:os:M:cancelTimer', timerID).take_none()


def setAlarm(time: LuaNum) -> int:
    # takes time of the day in hours 0..24
    # returns integer alarmID
    return eval_lua(b'G:os:M:setAlarm', time).take_int()


def cancelAlarm(alarmID: int) -> None:
    return eval_lua(b'G:os:M:cancelAlarm', alarmID).take_none()


def shutdown() -> None:
    return eval_lua(b'G:os:M:shutdown').take_none()


def reboot() -> None:
    return eval_lua(b'G:os:M:reboot').take_none()
