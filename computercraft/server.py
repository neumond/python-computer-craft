import argparse
import asyncio
import json
from os.path import join, dirname, abspath

from aiohttp import web, WSMsgType

from .sess import CCSession


THIS_DIR = dirname(abspath(__file__))
LUA_FILE = join(THIS_DIR, 'back.lua')


class CCApplication(web.Application):
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

            def sender(data):
                asyncio.create_task(ws.send_json(data))

            sess = CCSession(msg['computer'], sender)
            if msg['args']:
                sess.run_program(msg['args'][0])
            else:
                sess.run_repl()
            return sess

    async def ws(self, request):
        ws = web.WebSocketResponse()
        await ws.prepare(request)

        sess = await self._launch_program(ws)
        if sess is not None:
            async for msg in self._json_messages(ws):
                if msg['action'] == 'event':
                    sess.on_event(msg['event'], msg['params'])
                elif msg['action'] == 'task_result':
                    sess.on_task_result(msg['task_id'], msg['result'])
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
