from typing import Any, Tuple
from uuid import UUID

from . import lua


__all__ = (
    'serialize',
    'deserialize',
)


_ENC = 'latin1'
# encoding fast check
assert [bytes([i]) for i in range(256)] == [chr(i).encode(_ENC) for i in range(256)]


def encode(s: str) -> bytes:
    return s.encode(_ENC)


def u_encode(s: str) -> bytes:
    return s.encode('utf-8')


def u_encode_if_str(s: str) -> bytes:
    if isinstance(s, str):
        return s.encode('utf-8')
    return s


def nil_encode(s):
    if s is None:
        return None
    return encode(s)


def dirty_encode(s: str) -> bytes:
    return s.encode(_ENC, errors='replace')


def u_dirty_encode(s: str) -> bytes:
    return s.encode('utf-8', errors='replace')


def decode(b):
    return b.decode(_ENC)


def u_decode(b):
    return b.decode('utf-8')


def serialize(v: Any) -> bytes:
    if v is None:
        return b'N'
    elif v is False:
        return b'F'
    elif v is True:
        return b'T'
    elif isinstance(v, (int, float)):
        return '[{}]'.format(v).encode('ascii')
    elif isinstance(v, bytes):
        return '<{}>'.format(len(v)).encode('ascii') + v
    elif isinstance(v, UUID):
        return serialize(str(v).encode('ascii'))
    elif isinstance(v, str):
        raise ValueError('Strings are not allowed for serialization')
    elif isinstance(v, (list, tuple)):
        items = []
        for k, x in enumerate(v, start=1):
            items.append(b':' + serialize(k) + serialize(x))
        return b'{' + b''.join(items) + b'}'
    elif isinstance(v, dict):
        items = []
        for k, x in v.items():
            items.append(b':' + serialize(k) + serialize(x))
        return b'{' + b''.join(items) + b'}'
    elif isinstance(v, lua.LuaExpr):
        code = v.get_expr_code()
        return 'E{}>'.format(len(code)).encode('ascii') + code
    else:
        raise ValueError('Value can\'t be serialized: {}'.format(repr(v)))


def _deserialize(b: bytes, _idx: int) -> Tuple[Any, int]:
    tok = b[_idx]
    _idx += 1
    if tok == 78:  # N
        return None, _idx
    elif tok == 70:  # F
        return False, _idx
    elif tok == 84:  # T
        return True, _idx
    elif tok == 91:  # [
        newidx = b.index(b']', _idx)
        f = float(b[_idx:newidx])
        if f.is_integer():
            f = int(f)
        return f, newidx + 1
    elif tok == 60:  # <
        newidx = b.index(b'>', _idx)
        ln = int(b[_idx:newidx])
        return b[newidx + 1:newidx + 1 + ln], newidx + 1 + ln
    elif tok == 123:  # {
        r = {}
        while True:
            tok = b[_idx]
            _idx += 1
            if tok == 125:  # }
                break
            key, _idx = _deserialize(b, _idx)
            value, _idx = _deserialize(b, _idx)
            r[key] = value
        return r, _idx
    else:
        raise ValueError


def deserialize(b: bytes) -> Any:
    return _deserialize(b, 0)[0]


def dcmditer(b: bytes):
    yield b[0:1]
    idx = 1
    while idx < len(b):
        chunk, idx = _deserialize(b, idx)
        yield chunk
