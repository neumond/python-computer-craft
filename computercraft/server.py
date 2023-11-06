import argparse
import asyncio
from os.path import join, dirname, abspath

from aiohttp import web, WSMsgType

from . import ser, sess
from .rproc import lua_table_to_list


THIS_DIR = dirname(abspath(__file__))
LUA_FILE = join(THIS_DIR, 'back.lua')
PROTO_VERSION = 5
PROTO_ERROR = b'C' + ser.serialize(b'protocol error', 'ascii')


def protocol(send, sess_cls=sess.CCSession, oc=False):
    # handle first frame
    msg = yield
    msg = ser.dcmditer(msg)

    action = next(msg)
    if action != b'0':
        send(PROTO_ERROR)
        return

    version = next(msg)
    if version != PROTO_VERSION:
        send(b'C' + ser.serialize(
            'protocol version mismatch (expected {}, got {}), redownload py'.format(
                PROTO_VERSION, version,
            ), 'ascii'))
        return

    # CC:T starts its "args" with 0, includes program name
    # but {...} works normally, starting from 1
    args = next(msg)
    args = lua_table_to_list(args, low_index=0 if 0 in args else 1)
    path, code = None, None
    try:
        path = next(msg)
        code = next(msg)
    except StopIteration:
        pass
    sess = sess_cls(send, oc=oc)
    if code is not None:
        sess.run_program(args, path, code)
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
        elif action == b'C':
            sess.throw_keyboard_interrupt()
        else:
            send(PROTO_ERROR)
            return


class CCApplication(web.Application):
    async def ws(self, request):
        ws = web.WebSocketResponse()
        await ws.prepare(request)

        squeue = []
        pgen = self['protocol_factory'](squeue.append, oc=False)
        next(pgen)
        mustquit = False
        async for msg in ws:
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
        squeue = []

        def send(m):
            squeue.append(m)

        pgen = self['protocol_factory'](squeue.append, oc=True)
        next(pgen)
        mustquit = False
        while True:
            try:
                frame_size = int.from_bytes(
                    await reader.readexactly(3), 'big')
                frame = await reader.readexactly(frame_size)
            except asyncio.IncompleteReadError:
                break

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


def create_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('--host', default='0.0.0.0')
    parser.add_argument(
        '--port', type=int, default=8000,
        help='Web (for wget) & websocket (for computercraft) port')
    parser.add_argument(
        '--oc-port', type=int, default=8001,
        help='Raw TCP port for opencomputers')
    parser.add_argument(
        '--capture', type=str, default=None,
        help='Capture test data into a file')
    return parser


def main():
    args = create_parser().parse_args()
    app = CCApplication()
    app['port'] = args.port
    app['oc_port'] = args.oc_port
    app['protocol_factory'] = protocol
    app.setup_routes()

    async def tcp_server(app):
        server = await asyncio.start_server(app.tcp, args.host, args.oc_port)
        async with server:
            yield

    async def capture(app):
        with open(args.capture, 'wb') as f:
            def protocol_factory(send, sess_cls=sess.CCSession, oc=False):
                def write_frame(t, m):
                    ln = str(len(m)).encode('ascii')
                    f.write(t + ln + b':' + m + b'\n')

                def send_wrap(m):
                    write_frame(b'S', m)
                    return send(m)

                class SessOverride(sess_cls):
                    _drop_command = sess_cls._sorted_drop_command

                p = protocol(send_wrap, sess_cls=SessOverride, oc=oc)

                def pgen():
                    next(p)
                    while True:
                        m = yield
                        write_frame(b'R', m)
                        p.send(m)

                return pgen()

            app['protocol_factory'] = protocol_factory
            yield

    app.cleanup_ctx.append(tcp_server)
    if args.capture is not None:
        sess.python_version = lambda: '<VERSION>'
        app.cleanup_ctx.append(capture)

    with sess.patch_std_files():
        web.run_app(app, host=args.host, port=args.port)


if __name__ == '__main__':
    main()


# TODO: move greenlets into separate thread
# to prevent hanging

"""
import ctypes
import time
import threading

def thmain():
    # hangs
    while True:
        pass

th = threading.Thread(target=thmain)
th.start()
time.sleep(5)
ctypes.pythonapi.PyThreadState_SetAsyncExc(
    ctypes.c_long(th.ident),
    ctypes.py_object(TimeoutError))
time.sleep(3)
"""
