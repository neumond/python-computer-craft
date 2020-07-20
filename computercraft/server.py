import argparse
import asyncio
import sys
from os.path import join, dirname, abspath

from aiohttp import web, WSMsgType

from .sess import CCSession
from . import ser


THIS_DIR = dirname(abspath(__file__))
LUA_FILE = join(THIS_DIR, 'back.lua')
LUA_FILE_VERSION = 1


class CCApplication(web.Application):
    @staticmethod
    async def _bin_messages(ws):
        async for msg in ws:
            if msg.type != WSMsgType.BINARY:
                continue
            sys.__stdout__.write('ws received ' + repr(msg.data) + '\n')
            yield msg.data

    async def _launch_program(self, ws):
        async for msg in self._bin_messages(ws):
            msg = ser.deserialize(msg)
            if msg[b'action'] != b'run':
                await ws.send_bytes(ser.serialize({
                    'action': 'close',
                    'error': 'protocol error\n',
                }))
                return None
            if msg.get(b'version') != LUA_FILE_VERSION:
                await ws.send_bytes(ser.serialize({
                    'action': 'close',
                    'error': 'protocol version mismatch (expected {}, got {}), redownload py\n'.format(
                        LUA_FILE_VERSION, msg.get(b'version'),
                    ),
                }))
                return None

            def sender(data):
                sys.__stdout__.write('ws send ' + repr(data) + '\n')
                asyncio.create_task(ws.send_bytes(data))

            sess = CCSession(msg[b'computer'], sender)
            if msg[b'args']:
                sess.run_program(msg[b'args'][1].decode('latin1'))
            else:
                sess.run_repl()
            return sess

    async def ws(self, request):
        ws = web.WebSocketResponse()
        await ws.prepare(request)

        sess = await self._launch_program(ws)
        if sess is not None:
            async for msg in self._bin_messages(ws):
                msg = ser.deserialize(msg)
                if msg[b'action'] == b'event':
                    sess.on_event(msg[b'event'].decode('latin1'), msg[b'params'])
                elif msg[b'action'] == b'task_result':
                    sess.on_task_result(msg[b'task_id'].decode('latin1'), msg[b'result'])
                else:
                    await ws.send_bytes(ser.serialize({
                        'action': 'close',
                        'error': 'protocol error',
                    }))
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

    def initialize(self):
        self.router.add_get('/', self.backdoor)
        self.router.add_get('/ws/', self.ws)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--host')
    parser.add_argument('--port', type=int, default=8080)
    args = parser.parse_args()

    app_kw = {}
    if args.host is not None:
        app_kw['host'] = args.host
    app_kw['port'] = args.port

    app = CCApplication()
    app['port'] = args.port
    app.initialize()
    web.run_app(app, **app_kw)


if __name__ == '__main__':
    main()
