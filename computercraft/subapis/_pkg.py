from types import ModuleType

from ..errors import LuaException
from ..lua import lua_string
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
    mod = ModuleType(path)
    mod.__file__ = path
    path_expr = lua_string(path)
    if relative_to is not None:
        path_expr = 'fs.combine(fs.getDir({}), {})'.format(
            lua_string(relative_to),
            path_expr,
        )
    source = eval_lua('''
local p = {}
if not fs.exists(p) then return nil end
if fs.isDir(p) then return nil end
f = fs.open(p, "r")
local src = f.readAll()
f.close()
return src
'''.lstrip().format(
        path_expr,
    )).take_option_string()
    if source is None:
        raise ImportError('File not found: {}'.format(path))
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
