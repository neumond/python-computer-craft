from typing import Optional

from .. import ser
from ..lua import LuaNum
from ..sess import eval_lua_method_factory, get_current_greenlet


method = eval_lua_method_factory('os.')


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
    return method('version').take_string()


def getComputerID() -> int:
    return method('getComputerID').take_int()


def getComputerLabel() -> Optional[str]:
    return method('getComputerLabel').take_option_string()


def setComputerLabel(label: Optional[str]):
    return method('setComputerLabel', ser.nil_encode(label)).take_none()


def run(environment: dict, programPath: str, *args: str):
    args = tuple(ser.encode(a) for a in args)
    return method('run', environment, ser.encode(programPath), *args).take_bool()


def captureEvent(event: str):
    event = ser.encode(event)
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
    return method('queueEvent', ser.encode(event), *params).take_none()


def clock() -> LuaNum:
    # number of game ticks * 0.05, roughly seconds
    return method('clock').take_number()


# regarding ingame parameter below:
# python has great stdlib to deal with real current time
# we keep here only in-game time methods and parameters

def time() -> LuaNum:
    # in hours 0..24
    return method('time', b'ingame').take_number()


def day() -> int:
    return method('day', b'ingame').take_int()


def epoch() -> int:
    return method('epoch', b'ingame').take_int()


def sleep(seconds: LuaNum):
    return method('sleep', seconds).take_none()


def startTimer(timeout: LuaNum) -> int:
    return method('startTimer', timeout).take_int()


def cancelTimer(timerID: int):
    return method('cancelTimer', timerID).take_none()


def setAlarm(time: LuaNum) -> int:
    # takes time of the day in hours 0..24
    # returns integer alarmID
    return method('setAlarm', time).take_int()


def cancelAlarm(alarmID: int):
    return method('cancelAlarm', alarmID).take_none()


def shutdown():
    return method('shutdown').take_none()


def reboot():
    return method('reboot').take_none()
