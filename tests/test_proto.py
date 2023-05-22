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


_proto_folder = (Path(__file__).parent / 'proto')


@pytest.mark.parametrize(
    'logfile',
    _proto_folder.glob('**/*.txt'),
    ids=lambda p: str(p.relative_to(_proto_folder)))
def test_proto(logfile):
    sbuf = deque()
    with computercraft.sess.patch_std_files():
        pgen = computercraft.server.protocol(sbuf.append, oc='_oc' in logfile.name)
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
                    pgen.send(read_frame())
                elif t == b'S':
                    assert read_frame() == sbuf.popleft()
                else:
                    raise ValueError('Bad prefix ' + repr(t))

    assert len(sbuf) == 0
