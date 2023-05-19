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
        pgen = computercraft.server.protocol(sbuf.append)
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
                match lf.read(1):
                    case b'':
                        break
                    case b'R':
                        pgen.send(read_frame())
                    case b'S':
                        assert read_frame() == sbuf.popleft()
                    case _ as x:
                        raise ValueError('Bad prefix ' + repr(x))

    assert len(sbuf) == 0
