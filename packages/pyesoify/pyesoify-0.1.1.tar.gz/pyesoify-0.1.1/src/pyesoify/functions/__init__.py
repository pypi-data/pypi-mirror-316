"""
I've used __builtins__ extensively without obfuscation. This is because the obfuscation of __builtins__ is not necessary (it's tricky, too).
"""
from .print import PRINT 
from ._str import STR 
from .chr import CHR
from .getattr import GETATTR
from .map import MAP
import sys
sys.path.append('..')

from string_factory import make_string 

def make_function(name: str):
    return f"__builtins__.__getitem__({make_string(name)})"

SUPPORTED_FUNCTIONS: dict[str, str] = {
    'print': PRINT,
    'str': STR,
    'chr': CHR,
    'getattr': GETATTR,
    'map': MAP,
    'abs': make_function('abs'),
    'all': make_function('all'),
    'any': make_function('any'),
    'ascii': make_function('ascii'),
    'bin': make_function('bin'),
    'bool': make_function('bool'),
    'bytearray': make_function('bytearray'),
    'bytes': make_function('bytes'),
    'callable': make_function('callable'),
    'compile': make_function('compile'),
    'complex': make_function('complex'),
    'delattr': make_function('delattr'),
    'dict': make_function('dict'),
    'dir': make_function('dir'),
    'divmod': make_function('divmod'),
    'enumerate': make_function('enumerate'),
    'eval': make_function('eval'),
    'filter': make_function('filter'),
    'float': make_function('float'),
    'format': make_function('format'),
    'frozenset': make_function('frozenset'),
    'getattr': make_function('getattr'),
    'globals': make_function('globals'),
    'hasattr': make_function('hasattr'),
    'hash': make_function('hash'),
    'help': make_function('help'),
    'hex': make_function('hex'),
    'id': make_function('id'),
    'input': make_function('input'),
    'int': make_function('int'),
    'isinstance': make_function('isinstance'),
    'issubclass': make_function('issubclass'),
    'iter': make_function('iter'),
    'len': make_function('len'),
    'list': make_function('list'),
    'locals': make_function('locals'),
    'max': make_function('max'),
    'memoryview': make_function('memoryview'),
    'min': make_function('min'),
    'next': make_function('next'),
    'object': make_function('object'),
    'oct': make_function('oct'),
    'open': make_function('open'),
    'ord': make_function('ord'),
    'pow': make_function('pow'),
    'property': make_function('property'),
    'range': make_function('range'),
    'repr': make_function('repr'),
    'reversed': make_function('reversed'),
    'round': make_function('round'),
    'set': make_function('set'),
    'setattr': make_function('setattr'),
    'slice': make_function('slice'),
    'sorted': make_function('sorted'),
    'staticmethod': make_function('staticmethod'),
    'sum': make_function('sum'),
    'super': make_function('super'),
    'tuple': make_function('tuple'),
    'type': make_function('type'),
    'vars': make_function('vars'),
    'zip': make_function('zip'),
    'exec': make_function('exec'),
    'exit': make_function('exit'),
    'quit': make_function('quit'),
}

def obfs_function(func_name: str) -> str:
    return SUPPORTED_FUNCTIONS.get(func_name, func_name)
