import pytest

import computercraft.server
import computercraft.sess
from computercraft.ser import deserialize


@pytest.fixture
def protocol_tuple():
    sbuf = []

    def send(m):
        sbuf.append(deserialize(m))

    pgen = computercraft.server.protocol(sbuf.append)
    pgen.send(None)
    return pgen.send, sbuf


@pytest.fixture
def send(protocol_tuple):
    return protocol_tuple[0]


@pytest.fixture
def buf(protocol_tuple):
    return protocol_tuple[1]
