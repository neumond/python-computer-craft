from contextlib import asynccontextmanager
from typing import Optional, List

from .base import (
    BaseSubAPI, LuaTable, LuaNum,
    nil_return, str_return, opt_str_return, number_return, int_return, bool_return
)


class CCEventQueue:
    def __init__(self, q):
        self._q = q

    def __aiter__(self):
        return self

    async def __anext__(self):
        return await self._q.get()


class OSAPI(BaseSubAPI):
    _API = 'os'

    async def version(self) -> str:
        return str_return(await self._send('version'))

    async def getComputerID(self) -> int:
        return int_return(await self._send('getComputerID'))

    async def getComputerLabel(self) -> Optional[str]:
        return opt_str_return(await self._send('getComputerLabel'))

    async def setComputerLabel(self, label: Optional[str]):
        return nil_return(await self._send('setComputerLabel', label, omit_nulls=False))

    async def run(self, environment: LuaTable, programPath: str, *args: List[str]):
        return bool_return(await self._send('run', environment, programPath, *args))

    @asynccontextmanager
    async def captureEvent(self, targetEvent: str) -> CCEventQueue:
        '''
        Use this function instead loop over pullEvent/pullEventRaw.

        This makes a queue capable of effective event translation, excluding roundtrip delay.
        E.g.:
        1. You start short timer using os.startTimer().
        2. Then you call os.pullEvent() in loop to catch timer event.

        There exist some dead intervals of time, while pullEvent is going to be transferred to python side.
        Lua side can receive and discard timer event since there's no consumer for it.

        captureEvent gives you reliable way of receiving events without losses.
        Register queue before firing a timer, start a timer, listen for messages in queue.

        # it's significant here: start queue before starting a timer
        async with api.os.captureEvent('timer') as timer_queue:
            myTimer = await api.os.startTimer(3)
            async for etid, in timer_queue:
                if etid == myTimer:
                    await api.print('Timer reached')
                    break
        '''
        q, tid = await self._cc._start_queue(targetEvent)
        try:
            yield CCEventQueue(q)
        finally:
            await self._cc._stop_queue(tid)

    async def queueEvent(self, event: str, *params):
        return nil_return(await self._send('queueEvent', event, *params, omit_nulls=False))

    async def clock(self) -> LuaNum:
        # number of game ticks * 0.05, roughly seconds
        return number_return(await self._send('clock'))

    # regarding ingame parameter below:
    # python has great stdlib to deal with real current time
    # we keep here only in-game time methods and parameters

    async def time(self) -> LuaNum:
        # in hours 0..24
        return number_return(await self._send('time', 'ingame'))

    async def day(self) -> int:
        return int_return(await self._send('day', 'ingame'))

    async def epoch(self) -> int:
        return int_return(await self._send('epoch', 'ingame'))

    async def sleep(self, seconds: LuaNum):
        return nil_return(await self._send('sleep', seconds))

    async def startTimer(self, timeout: LuaNum) -> int:
        return int_return(await self._send('startTimer', timeout))

    async def cancelTimer(self, timerID: int):
        return nil_return(await self._send('cancelTimer', timerID))

    async def setAlarm(self, time: LuaNum) -> int:
        # takes time of the day in hours 0..24
        # returns integer alarmID
        return int_return(await self._send('setAlarm', time))

    async def cancelAlarm(self, alarmID: int):
        return nil_return(await self._send('cancelAlarm', alarmID))

    async def shutdown(self):
        return nil_return(await self._send('shutdown'))

    async def reboot(self):
        return nil_return(await self._send('reboot'))
