from types import ModuleType

from ..errors import LuaException
from ..sess import eval_lua


__all__ = (
    'import_file',
    'is_commands',
    'is_multishell',
    'is_turtle',
    'is_pocket',
    'eval_lua',
    'LuaException',
)


def import_file(path: str, relative_to: str = None):
    source = eval_lua(b'''
local p, rel = ...
if rel ~= nil then
p = fs.combine(fs.getDir(rel), p)
end
if not fs.exists(p) then return nil end
if fs.isDir(p) then return nil end
f = fs.open(p, "r")
local src = f.readAll()
f.close()
return src
'''.strip(), path, relative_to).take_option_string()
    if source is None:
        raise ImportError('File not found: {}'.format(path))
    mod = ModuleType(path)
    mod.__file__ = path
    cc = compile(source, mod.__name__, 'exec')
    exec(cc, vars(mod))
    return mod


def is_commands() -> bool:
    return eval_lua(b'return commands ~= nil').take_bool()


def is_multishell() -> bool:
    return eval_lua(b'return multishell ~= nil').take_bool()


def is_turtle() -> bool:
    return eval_lua(b'return turtle ~= nil').take_bool()


def is_pocket() -> bool:
    return eval_lua(b'return pocket ~= nil').take_bool()
