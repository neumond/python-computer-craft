import asyncio
import json
import string
from aiohttp import web
from traceback import print_exc
from os.path import join, dirname, abspath
from importlib import import_module
import argparse

from .subapis.root import RootAPIMixin
from .errors import LuaException

from .subapis.colors import ColorsAPI
from .subapis.commands import CommandsAPI
from .subapis.disk import DiskAPI
from .subapis.fs import FSAPI
from .subapis.gps import GpsAPI
from .subapis.help import HelpAPI
from .subapis.keys import KeysAPI
from .subapis.multishell import MultishellAPI
from .subapis.os import OSAPI
from .subapis.peripheral import PeripheralAPI
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


async def lua_json(request):
    body = await request.text()
    body = body.replace('\\\n', '\\n')
    return json.loads(body)


class CCAPI(RootAPIMixin):
    def __init__(self, nid, program, cleanup_callback):
        self._id = nid
        self._task_autoid = 1
        self._cmd = asyncio.Queue(maxsize=1)
        self._result_locks = {}
        self._result_values = {}
        self._result_queues = {}

        self.colors = ColorsAPI
        self.commands = CommandsAPI(self)
        self.disk = DiskAPI(self)
        self.fs = FSAPI(self)
        self.gps = GpsAPI(self)
        self.help = HelpAPI(self)
        self.keys = KeysAPI(self)
        self.multishell = MultishellAPI(self)
        self.os = OSAPI(self)
        self.peripheral = PeripheralAPI(self)
        self.rednet = RednetAPI(self)
        self.redstone = RedstoneAPI(self)
        self.settings = SettingsAPI(self)
        self.shell = ShellAPI(self)  # TODO: autocomplete functions
        self.term = TermAPI(self)  # TODO: window redirections
        self.textutils = TextutilsAPI(self)
        self.turtle = TurtleAPI(self)
        self.window = WindowAPI(self)  # TODO: unimplemented

        async def prog_wrap():
            cancel = False
            try:
                await program(self)
            except asyncio.CancelledError:
                print('program {} cancelled'.format(self._id))
                print_exc()
                cancel = True
            except Exception as e:
                print('program {} crashed: {} {}'.format(self._id, type(e), e))
                print_exc()
            else:
                print('program {} finished'.format(self._id))
            finally:
                if not cancel:
                    await self._cmd.put('END')
                cleanup_callback()

        self._task = asyncio.ensure_future(prog_wrap())

    def _new_task_id(self):
        task_id = base36(self._task_autoid)
        self._task_autoid += 1
        return task_id

    async def _send_cmd(self, lua):
        task_id = self._new_task_id()
        self._result_locks[task_id] = asyncio.Event()
        await self._cmd.put('TASK;' + task_id + ';' + lua)
        await self._result_locks[task_id].wait()
        del self._result_locks[task_id]
        result = self._result_values.pop(task_id)
        print('{} → {}'.format(lua, result))
        if not result[0]:
            raise LuaException(*result[1:])
        return result[1:]

    async def _start_queue(self, event):
        task_id = self._new_task_id()
        self._result_queues[task_id] = asyncio.Queue()
        await self._cmd.put('STARTQUEUE;' + task_id + ';' + event)
        return self._result_queues[task_id], task_id

    async def _stop_queue(self, task_id):
        await self._cmd.put('STOPQUEUE;' + task_id)
        del self._result_queues[task_id]


logging_config = '''
version: 1
disable_existing_loggers: false
root:
  level: ERROR
  handlers:
  - console
handlers:
  console:
    level: INFO
    class: logging.StreamHandler
    formatter: verbose
loggers:
  aiohttp.access:
    level: INFO
    handlers: []
    propagate: true
formatters:
  verbose:
    format: '%(message)s'
'''


def enable_request_logging():
    import logging.config
    import yaml
    logging.config.dictConfig(yaml.load(logging_config))


class CCApplication(web.Application):
    async def start(self, request):
        tid = int(request.match_info['turtle'])
        if tid in self['exchange']:
            # terminate old program
            self['exchange'][tid]._task.cancel()
        module = import_module(self['source_module'])
        program = getattr(module, request.match_info['program'])

        def cleanup_callback():
            del self['exchange'][tid]

        self['exchange'][tid] = CCAPI(tid, program, cleanup_callback)
        return web.Response(text='')

    async def gettask(self, request):
        api = self['exchange'].get(int(request.match_info['turtle']))
        if api is None:
            return web.Response(text='END')
        return web.Response(text=await api._cmd.get())

    async def taskresult(self, request):
        api = self['exchange'].get(int(request.match_info['turtle']))
        if api is not None:
            tid = request.match_info['task_id']
            if tid in api._result_locks:
                # it's a TASK
                api._result_values[tid] = await lua_json(request)
                api._result_locks[tid].set()
            elif tid in api._result_queues:
                # it's a QUEUE
                await api._result_queues[tid].put(await lua_json(request))
            # otherwise just ignore
        return web.Response(text='')

    @staticmethod
    def backdoor(request):
        with open(LUA_FILE, 'r') as f:
            fcont = f.read()
        fcont = fcont.replace(
            "local url = 'http://127.0.0.1:4343/'",
            "local url = '{}://{}/'".format(request.scheme, request.host)
        )
        return web.Response(text=fcont)

    def initialize(self, source_module):
        self['source_module'] = source_module
        self['exchange'] = {}
        self.router.add_get('/', self.backdoor)
        self.router.add_post('/start/{turtle}/{program}/', self.start)
        self.router.add_post('/gettask/{turtle}/', self.gettask)
        self.router.add_post('/taskresult/{turtle}/{task_id}/', self.taskresult)


def main():
    # enable_request_logging()

    parser = argparse.ArgumentParser()
    parser.add_argument('module', help='Module used as source for programs')
    parser.add_argument('--host')
    parser.add_argument('--port', type=int)
    args = parser.parse_args()

    app_kw = {}
    if args.host is not None:
        app_kw['host'] = args.host
    if args.port is not None:
        app_kw['port'] = args.port

    app = CCApplication()
    app.initialize(args.module)
    web.run_app(app, **app_kw)


if __name__ == '__main__':
    main()
