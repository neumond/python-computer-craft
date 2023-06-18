from typing import Union

from ..sess import eval_lua


# curl -s https://raw.githubusercontent.com/MightyPirates/OpenComputers/master-MC1.12/src/main/\
# resources/assets/opencomputers/loot/openos/lib/core/full_keyboard.lua \
# | grep -E '^keyboard\.keys' \
# | sed -E 's/^keyboard\.keys\.(\S+)\s*\=\s*([0-9A-Fx]+).*$/\2: '\''\1'\'',/' \
# | sed -E 's/^keyboard\.keys\["(\S+)"\]\s*\=\s*([0-9A-Fx]+).*$/\2: '\''\1'\'',/'

_index = {
    0x02: '1',
    0x03: '2',
    0x04: '3',
    0x05: '4',
    0x06: '5',
    0x07: '6',
    0x08: '7',
    0x09: '8',
    0x0A: '9',
    0x0B: '0',
    0x1E: 'a',
    0x30: 'b',
    0x2E: 'c',
    0x20: 'd',
    0x12: 'e',
    0x21: 'f',
    0x22: 'g',
    0x23: 'h',
    0x17: 'i',
    0x24: 'j',
    0x25: 'k',
    0x26: 'l',
    0x32: 'm',
    0x31: 'n',
    0x18: 'o',
    0x19: 'p',
    0x10: 'q',
    0x13: 'r',
    0x1F: 's',
    0x14: 't',
    0x16: 'u',
    0x2F: 'v',
    0x11: 'w',
    0x2D: 'x',
    0x15: 'y',
    0x2C: 'z',
    0x28: 'apostrophe',
    0x91: 'at',
    0x0E: 'back',
    0x2B: 'backslash',
    0x3A: 'capital',
    0x92: 'colon',
    0x33: 'comma',
    0x1C: 'enter',
    0x0D: 'equals',
    0x29: 'grave',
    0x1A: 'lbracket',
    0x1D: 'lcontrol',
    0x38: 'lmenu',
    0x2A: 'lshift',
    0x0C: 'minus',
    0x45: 'numlock',
    0xC5: 'pause',
    0x34: 'period',
    0x1B: 'rbracket',
    0x9D: 'rcontrol',
    0xB8: 'rmenu',
    0x36: 'rshift',
    0x46: 'scroll',
    0x27: 'semicolon',
    0x35: 'slash',
    0x39: 'space',
    0x95: 'stop',
    0x0F: 'tab',
    0x93: 'underline',
    0xC8: 'up',
    0xD0: 'down',
    0xCB: 'left',
    0xCD: 'right',
    0xC7: 'home',
    0xCF: 'end',
    0xC9: 'pageUp',
    0xD1: 'pageDown',
    0xD2: 'insert',
    0xD3: 'delete',
    0x3B: 'f1',
    0x3C: 'f2',
    0x3D: 'f3',
    0x3E: 'f4',
    0x3F: 'f5',
    0x40: 'f6',
    0x41: 'f7',
    0x42: 'f8',
    0x43: 'f9',
    0x44: 'f10',
    0x57: 'f11',
    0x58: 'f12',
    0x64: 'f13',
    0x65: 'f14',
    0x66: 'f15',
    0x67: 'f16',
    0x68: 'f17',
    0x69: 'f18',
    0x71: 'f19',
    0x70: 'kana',
    0x94: 'kanji',
    0x79: 'convert',
    0x7B: 'noconvert',
    0x7D: 'yen',
    0x90: 'circumflex',
    0x96: 'ax',
    0x52: 'numpad0',
    0x4F: 'numpad1',
    0x50: 'numpad2',
    0x51: 'numpad3',
    0x4B: 'numpad4',
    0x4C: 'numpad5',
    0x4D: 'numpad6',
    0x47: 'numpad7',
    0x48: 'numpad8',
    0x49: 'numpad9',
    0x37: 'numpadmul',
    0xB5: 'numpaddiv',
    0x4A: 'numpadsub',
    0x4E: 'numpadadd',
    0x53: 'numpaddecimal',
    0xB3: 'numpadcomma',
    0x9C: 'numpadenter',
    0x8D: 'numpadequals',
}


class Keys:
    def __getitem__(self, key: int) -> str:
        return _index[key]

    def __iter__(self):
        return iter(_index.items())

    def __len__(self):
        return len(_index)


for i, v in _index.items():
    setattr(Keys, v, i)
del i, v
keys = Keys()


def isAltDown() -> bool:
    return eval_lua(b'R:keyboard:M:isAltDown').take_bool_coerce_nil()


def isControl(char: int) -> bool:
    return eval_lua(b'R:keyboard:M:isControl', char).take_bool()


def isControlDown() -> bool:
    return eval_lua(b'R:keyboard:M:isControlDown').take_bool_coerce_nil()


def isKeyDown(charOrCode: Union[int, str]) -> bool:
    return eval_lua(b'R:keyboard:M:isKeyDown', charOrCode).take_bool_coerce_nil()


def isShiftDown() -> bool:
    return eval_lua(b'R:keyboard:M:isShiftDown').take_bool_coerce_nil()


__all__ = (
    'keys',
    'isAltDown',
    'isControl',
    'isControlDown',
    'isKeyDown',
    'isShiftDown',
)
