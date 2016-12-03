from typing import Optional, List
from .base import (
    BaseSubAPI, LuaTable, LuaNum,
    nil_return, str_return, opt_str_return, number_return, int_return, bool_return
)


class CCEventQueue(BaseSubAPI):
    def __init__(self, cc, targetEvent):
        super().__init__(cc)
        self._targetEvent = targetEvent

    async def __aenter__(self):
        self._q, self._tid = await self._cc._start_queue(self._targetEvent)
        return self

    async def __aexit__(self, exc_type, exc, tb):
        await self._cc._stop_queue(self._tid)

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

    async def loadAPI(self, path: str):
        return bool_return(await self._send('loadAPI', path))

    async def unloadAPI(self, name: str):
        return nil_return(await self._send('unloadAPI', name))

    def registerEventQueue(self, targetEvent: str) -> CCEventQueue:
        '''
        Use this function instead loop over pullEvent/pullEventRaw.

        This makes a queue capable of effective event translation, excluding roundtrip delay.
        E.g.:
        1. You start short timer using os.startTimer().
        2. Then you call os.pullEvent() in loop to catch timer event.

        There exist some dead intervals of time, while pullEvent is going to be transferred to python side.
        Lua side can receive and discard timer event since there's no consumer for it.

        registerEventQueue gives you reliable way of receiving events without losses.
        Register queue before firing a timer, start a timer, listen for messages in queue.

        # it's significant here: start queue before starting a timer
        async with api.os.registerEventQueue('timer') as timer_queue:
            myTimer = await api.os.startTimer(3)
            async for e in timer_queue:
                if e[1] == myTimer:
                    await api.print('Timer reached')
                    break
        '''
        return CCEventQueue(self._cc, targetEvent)

    async def queueEvent(self, event: str, *params):
        return nil_return(await self._send('queueEvent', event, *params))

    async def clock(self) -> LuaNum:
        return number_return(await self._send('clock'))

    async def startTimer(self, timeout: LuaNum) -> int:
        return int_return(await self._send('startTimer', timeout))

    async def cancelTimer(self, timerID: int):
        return nil_return(await self._send('cancelTimer', timerID))

    async def time(self) -> LuaNum:
        return number_return(await self._send('time'))

    async def sleep(self, seconds: LuaNum):
        return nil_return(await self._send('sleep', seconds))

    async def day(self) -> int:
        return int_return(await self._send('day'))

    async def setAlarm(self, time: LuaNum) -> int:
        return int_return(await self._send('setAlarm', time))

    async def cancelAlarm(self, alarmID: int):
        return nil_return(await self._send('cancelAlarm', alarmID))

    async def shutdown(self):
        return nil_return(await self._send('shutdown'))

    async def reboot(self):
        return nil_return(await self._send('reboot'))
