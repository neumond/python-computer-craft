import asyncio
import json
import string
from aiohttp import web, WSMsgType
from contextlib import asynccontextmanager
from traceback import print_exc
from os.path import join, dirname, abspath
from importlib import import_module
import argparse

from .subapis.root import RootAPIMixin
from .lua import lua_string
from . import rproc

from .subapis.colors import ColorsAPI
from .subapis.commands import CommandsAPI
from .subapis.disk import DiskAPI
from .subapis.fs import FSAPI
from .subapis.gps import GpsAPI
from .subapis.help import HelpAPI
from .subapis.keys import KeysAPI
from .subapis.multishell import MultishellAPI
from .subapis.os import OSAPI
from .subapis.paintutils import PaintutilsAPI
from .subapis.peripheral import PeripheralAPI
from .subapis.pocket import PocketAPI
from .subapis.rednet import RednetAPI
from .subapis.redstone import RedstoneAPI
from .subapis.settings import SettingsAPI
from .subapis.shell import ShellAPI
from .subapis.term import TermAPI
from .subapis.textutils import TextutilsAPI
from .subapis.turtle import TurtleAPI
from .subapis.window import WindowAPI


THIS_DIR = dirname(abspath(__file__))
LUA_FILE = join(THIS_DIR, 'back.lua')
DIGITS = string.digits + string.ascii_lowercase


def base36(n):
    r = ''
    while n:
        r += DIGITS[n % 36]
        n //= 36
    return r[::-1]


class CCAPI(RootAPIMixin):
    def __init__(self, nid, program, cleanup_callback):
        self._id = nid
        self._task_autoid = 1
        self._cmd = asyncio.Queue(maxsize=1)
        self._result_locks = {}
        self._result_values = {}
        self._result_queues = {}
        self._event_to_tids = {}
        self._tid_to_event = {}

        self.colors = ColorsAPI(self, 'colors')
        self.commands = CommandsAPI(self, 'commands')
        self.disk = DiskAPI(self, 'disk')
        self.fs = FSAPI(self, 'fs')
        self.gps = GpsAPI(self, 'gps')
        self.help = HelpAPI(self, 'help')
        self.keys = KeysAPI(self, 'keys')
        self.multishell = MultishellAPI(self, 'multishell')
        self.os = OSAPI(self, 'os')
        self.paintutils = PaintutilsAPI(self, 'paintutils')
        self.peripheral = PeripheralAPI(self, 'peripheral')
        self.pocket = PocketAPI(self, 'pocket')
        self.rednet = RednetAPI(self, 'rednet')
        self.redstone = RedstoneAPI(self, 'redstone')
        self.settings = SettingsAPI(self, 'settings')
        self.shell = ShellAPI(self, 'shell')
        self.term = TermAPI(self, 'term')
        self.textutils = TextutilsAPI(self, 'textutils')
        self.turtle = TurtleAPI(self, 'turtle')
        self.window = WindowAPI(self, 'window')

        async def prog_wrap():
            err = None
            try:
                await program(self)
            except asyncio.CancelledError:
                print('program {} cancelled'.format(self._id))
                print_exc()
                err = 'program has been cancelled'
            except Exception as e:
                print('program {} crashed: {} {}'.format(self._id, type(e), e))
                print_exc()
                err = type(e).__name__ + ': ' + str(e)
            else:
                print('program {} finished'.format(self._id))
            finally:
                c = {'action': 'close'}
                if err is not None:
                    c['error'] = err
                await self._cmd.put(c)
                cleanup_callback()

        self._task = asyncio.create_task(prog_wrap())

    def _new_task_id(self) -> str:
        task_id = base36(self._task_autoid)
        self._task_autoid += 1
        return task_id

    async def _eval(self, lua_code, immediate=False):
        task_id = self._new_task_id()
        self._result_locks[task_id] = asyncio.Event()
        await self._cmd.put({
            'action': 'task',
            'task_id': task_id,
            'code': lua_code,
            'immediate': immediate,
        })
        await self._result_locks[task_id].wait()
        del self._result_locks[task_id]
        result = self._result_values.pop(task_id)
        print('{} → {}'.format(lua_code, repr(result)))
        return result

    async def eval(self, lua_code):
        return await self._eval(lua_code, True)

    async def eval_coro(self, lua_code):
        return rproc.coro(await self._eval(lua_code, False))

    async def _start_queue(self, event):
        task_id = self._new_task_id()
        self._result_queues[task_id] = asyncio.Queue()
        es = self._event_to_tids.setdefault(event, set())
        if not es:
            await self._cmd.put({
                'action': 'sub',
                'event': event,
            })
        es.add(task_id)
        self._tid_to_event[task_id] = event
        return self._result_queues[task_id], task_id

    async def _stop_queue(self, task_id):
        event = self._tid_to_event[task_id]
        del self._result_queues[task_id]
        del self._tid_to_event[task_id]
        self._event_to_tids[event].discard(task_id)
        if not self._event_to_tids[event]:
            await self._cmd.put({
                'action': 'unsub',
                'event': event,
            })

    @asynccontextmanager
    async def _create_temp_object(self, create_expr: str, finalizer_template: str = ''):
        fid = self._new_task_id()
        var = 'temp[{}]'.format(lua_string(fid))
        await self.eval_coro('{} = {}'.format(var, create_expr))
        try:
            yield var
        finally:
            finalizer_template += '; {e} = nil'
            finalizer_template = finalizer_template.lstrip(' ;')
            await self.eval_coro(finalizer_template.format(e=var))


class CCApplication(web.Application):
    @staticmethod
    async def _sender(ws, api):
        while not ws.closed:
            cmd = await api._cmd.get()
            # print(f'_sender: {cmd}')
            if not ws.closed:
                await ws.send_json(cmd)
            if cmd['action'] == 'close':
                break

    @staticmethod
    async def _json_messages(ws):
        async for msg in ws:
            # print('ws received', msg)
            if msg.type != WSMsgType.TEXT:
                continue
            # print('ws received', msg.data)
            yield json.loads(msg.data.replace('\\\n', '\\n'))

    async def _launch_program(self, ws):
        async for msg in self._json_messages(ws):
            if msg['action'] != 'run':
                await ws.send_json({
                    'action': 'close',
                    'error': 'protocol error',
                })
                return None
            if len(msg['args']) == 0:
                await ws.send_json({
                    'action': 'close',
                    'error': 'arguments required',
                })
                return None
            module = import_module(self['source_module'])
            program = getattr(module, msg['args'][0], None)
            if program is None:
                await ws.send_json({
                    'action': 'close',
                    'error': "program doesn't exist",
                })
                return None
            return CCAPI(msg['computer'], program, lambda: None)

    async def ws(self, request):
        ws = web.WebSocketResponse()
        await ws.prepare(request)

        api = await self._launch_program(ws)
        if api is not None:
            asyncio.create_task(self._sender(ws, api))
            async for msg in self._json_messages(ws):
                if msg['action'] == 'event':
                    for task_id in api._event_to_tids.get(msg['event'], ()):
                        await api._result_queues[task_id].put(msg['params'])
                elif msg['action'] == 'task_result':
                    api._result_values[msg['task_id']] = msg['result']
                    api._result_locks[msg['task_id']].set()
                else:
                    await ws.send_json({
                        'action': 'close',
                        'error': 'protocol error',
                    })
                    break

        return ws

    @staticmethod
    def backdoor(request):
        with open(LUA_FILE, 'r') as f:
            fcont = f.read()
        h = request.host
        if ':' not in h:
            # fix for malformed Host header
            h += ':{}'.format(request.app['port'])
        fcont = fcont.replace(
            "local url = 'http://127.0.0.1:4343/'",
            "local url = '{}://{}/'".format('ws', h)
        )
        return web.Response(text=fcont)

    def initialize(self, source_module):
        self['source_module'] = source_module
        self['exchange'] = {}
        self.router.add_get('/', self.backdoor)
        self.router.add_get('/ws/', self.ws)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('module', help='Module used as source for programs')
    parser.add_argument('--host')
    parser.add_argument('--port', type=int, default=8080)
    args = parser.parse_args()

    app_kw = {}
    if args.host is not None:
        app_kw['host'] = args.host
    app_kw['port'] = args.port

    app = CCApplication()
    app['port'] = args.port
    app.initialize(args.module)
    web.run_app(app, **app_kw)


if __name__ == '__main__':
    main()
