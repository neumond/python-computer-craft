from collections import deque
from pathlib import Path

import pytest

import computercraft.server
import computercraft.sess


@pytest.fixture(autouse=True)
def _patch(monkeypatch):
    monkeypatch.setattr(
        computercraft.sess, 'python_version',
        lambda: '<VERSION>')
    monkeypatch.setattr(
        computercraft.sess.CCSession, '_drop_command',
        computercraft.sess.CCSession._sorted_drop_command)


_proto_folder = (Path(__file__).parent / 'proto')


@pytest.mark.parametrize(
    'logfile',
    _proto_folder.glob('**/*.txt'),
    ids=lambda p: str(p.relative_to(_proto_folder)))
def test_proto(logfile):
    sbuf = deque()
    with computercraft.sess.patch_std_files():
        pgen = computercraft.server.protocol(
            sbuf.append,
            oc='/oc_' in str(logfile.relative_to(_proto_folder)))
        pgen.send(None)

        with logfile.open('rb') as lf:

            def read_frame():
                flen = []
                while (b := lf.read(1)) != b':':
                    flen.append(b)
                flen = int(b''.join(flen))
                frame = lf.read(flen)
                assert len(frame) == flen
                assert lf.read(1) == b'\n'
                return frame

            while True:
                t = lf.read(1)
                if t == b'':
                    break
                elif t == b'R':
                    frame = read_frame()
                    try:
                        pgen.send(frame)
                    except StopIteration:
                        if frame == b'D':
                            break
                        pytest.fail(
                            'Protocol prematurely finished on frame ' + repr(frame))
                elif t == b'S':
                    assert read_frame() == sbuf.popleft()
                else:
                    raise ValueError('Bad prefix ' + repr(t))

    assert len(sbuf) == 0
