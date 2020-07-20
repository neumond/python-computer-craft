from typing import Any, Tuple


__all__ = (
    'serialize',
    'deserialize',
)


_ENC = 'latin1'
# encoding fast check
assert [bytes([i]) for i in range(256)] == [chr(i).encode(_ENC) for i in range(256)]


def serialize(v: Any) -> bytes:
    if v is None:
        return b'N'
    elif v is False:
        return b'F'
    elif v is True:
        return b'T'
    elif isinstance(v, (int, float)):
        return '[{}]'.format(v).encode(_ENC)
    elif isinstance(v, bytes):
        return '<{}>'.format(len(v)).encode(_ENC) + v
    elif isinstance(v, str):
        return '<{}>'.format(len(v)).encode(_ENC) + v.encode(_ENC)
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
    else:
        raise ValueError


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
