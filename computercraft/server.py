import argparse
import asyncio
import sys
from os.path import join, dirname, abspath

from aiohttp import web, WSMsgType

from .sess import CCSession
from . import ser
from .rproc import lua_table_to_list


THIS_DIR = dirname(abspath(__file__))
LUA_FILE = join(THIS_DIR, 'back.lua')
PROTO_VERSION = 4
PROTO_ERROR = b'C' + ser.serialize(b'protocol error')
DEBUG_PROTO = False


async def _bin_messages(ws):
    async for msg in ws:
        if msg.type != WSMsgType.BINARY:
            continue
        if DEBUG_PROTO:
            sys.__stdout__.write('ws received ' + repr(msg.data) + '\n')
        yield msg.data


async def _send(ws, data):
    if DEBUG_PROTO:
        sys.__stdout__.write('ws send ' + repr(data) + '\n')
    await ws.send_bytes(data)


def protocol(send, sess_cls=CCSession):
    # handle first frame
    msg = yield
    msg = ser.dcmditer(msg)

    action = next(msg)
    if action != b'0':
        send(PROTO_ERROR)
        return

    version = next(msg)
    if version != PROTO_VERSION:
        send(b'C' + ser.serialize(ser.encode(
            'protocol version mismatch (expected {}, got {}), redownload py'.format(
                PROTO_VERSION, version,
            ))))
        return

    args = lua_table_to_list(next(msg), low_index=0)
    sess = sess_cls(send)
    if len(args) >= 2:
        sess.run_program(args[1], [ser.decode(x) for x in args[2:]])
    else:
        sess.run_repl()

    # handle the rest of frames
    while True:
        msg = yield
        msg = ser.dcmditer(msg)
        action = next(msg)
        if action == b'E':
            sess.on_event(next(msg), lua_table_to_list(next(msg)))
        elif action == b'T':
            sess.on_task_result(next(msg), next(msg))
        else:
            send(PROTO_ERROR)
            return


class CCApplication(web.Application):
    async def ws(self, request):
        ws = web.WebSocketResponse()
        await ws.prepare(request)

        squeue = []
        pgen = protocol(squeue.append)
        next(pgen)
        mustquit = False
        async for msg in _bin_messages(ws):
            if msg.type != WSMsgType.BINARY:
                continue

            try:
                pgen.send(msg.data)
            except StopIteration:
                mustquit = True

            for m in squeue:
                await ws.send_bytes(m)
            squeue.clear()

            if mustquit:
                break
        return ws

    async def tcp(self, reader, writer):
        if DEBUG_PROTO:
            print('TCP connection')
        squeue = []

        def send(m):
            if DEBUG_PROTO:
                print('SEND', m)
            squeue.append(m)

        pgen = protocol(send)
        # pgen = protocol(squeue.append)
        next(pgen)
        mustquit = False
        while True:
            if DEBUG_PROTO:
                print('Waiting for frame')
            try:
                frame_size = int.from_bytes(
                    await reader.readexactly(3), 'big')
                frame = await reader.readexactly(frame_size)
            except asyncio.IncompleteReadError:
                break

            if DEBUG_PROTO:
                print('TCP frame', frame)

            try:
                pgen.send(frame)
            except StopIteration:
                mustquit = True

            for m in squeue:
                writer.write(len(m).to_bytes(3, 'big'))
                writer.write(m)
            squeue.clear()
            await writer.drain()

            if mustquit:
                break

        if DEBUG_PROTO:
            print('TCP close')
        writer.close()
        await writer.wait_closed()

    @staticmethod
    def backdoor(request):
        with open(LUA_FILE, 'r') as f:
            fcont = f.read()
        webhost = tcphost = request.host
        if ':' in request.host:
            tcphost = tcphost.rsplit(':', 1)[0]
        else:
            # fix for malformed Host header
            webhost += ':{}'.format(request.app['port'])
        return web.Response(text=(
            fcont
            .replace('__cc_url__', 'ws://{}/ws/'.format(webhost))
            .replace('__oc_host__', tcphost)
            .replace('__oc_port__', str(request.app['oc_port']))
        ))

    def setup_routes(self):
        self.router.add_get('/', self.backdoor)
        self.router.add_get('/ws/', self.ws)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--host', default='0.0.0.0')
    parser.add_argument(
        '--port', type=int, default=8000,
        help='Web (for wget) & websocket (for computercraft) port')
    parser.add_argument(
        '--oc-port', type=int, default=8001,
        help='Raw TCP port for opencomputers')
    args = parser.parse_args()

    app = CCApplication()
    app['port'] = args.port
    app['oc_port'] = args.oc_port
    app.setup_routes()

    async def tcp_server(app):
        server = await asyncio.start_server(app.tcp, args.host, args.oc_port)
        async with server:
            yield

    app.cleanup_ctx.append(tcp_server)

    web.run_app(app, host=args.host, port=args.port)


if __name__ == '__main__':
    main()
