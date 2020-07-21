import argparse
import asyncio
import sys
from os.path import join, dirname, abspath

from aiohttp import web, WSMsgType

from .sess import CCSession
from . import ser


THIS_DIR = dirname(abspath(__file__))
LUA_FILE = join(THIS_DIR, 'back.lua')
LUA_FILE_VERSION = 2
PROTO_ERROR = b'C' + ser.serialize('protocol error')
DEBUG_PROTO = True


class CCApplication(web.Application):
    @staticmethod
    async def _bin_messages(ws):
        async for msg in ws:
            if msg.type != WSMsgType.BINARY:
                continue
            if DEBUG_PROTO:
                sys.__stdout__.write('ws received ' + repr(msg.data) + '\n')
            yield msg.data

    @staticmethod
    async def _send(ws, data):
        if DEBUG_PROTO:
            sys.__stdout__.write('ws send ' + repr(data) + '\n')
        await ws.send_bytes(data)

    async def _launch_program(self, ws):
        async for msg in self._bin_messages(ws):
            msg = ser.dcmditer(msg)

            action = next(msg)
            if action != b'0':
                await self._send(ws, PROTO_ERROR)
                return None

            version = next(msg)
            if version != LUA_FILE_VERSION:
                await self._send(ws, b'C' + ser.serialize(
                    'protocol version mismatch (expected {}, got {}), redownload py'.format(
                        LUA_FILE_VERSION, version,
                    )))
                return None

            computer_id = next(msg)
            args = next(msg)

            def sender(data):
                asyncio.create_task(self._send(ws, data))

            sess = CCSession(computer_id, sender)
            if args.get(1):
                sess.run_program(args[1].decode('latin1'))
            else:
                sess.run_repl()
            return sess

    async def ws(self, request):
        ws = web.WebSocketResponse()
        await ws.prepare(request)

        sess = await self._launch_program(ws)
        if sess is not None:
            async for msg in self._bin_messages(ws):
                msg = ser.dcmditer(msg)
                action = next(msg)
                if action == b'E':
                    sess.on_event(
                        next(msg).decode('latin1'),
                        next(msg),
                    )
                elif action == b'T':
                    sess.on_task_result(
                        next(msg).decode('latin1'),
                        next(msg),
                    )
                else:
                    await self._send(ws, PROTO_ERROR)
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
