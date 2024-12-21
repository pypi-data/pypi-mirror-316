"""
print.py
~~~~~~~~

This module contains the print function.
`print` can be accessed through `__builtins__.__getattribute__("print")`.
So, our task is really to obfuscate `"print"` in the code.

We'll do this by obfuscating `''.join("print")`
Which is `str().join("print")`
=> `str().join(["p", "r", "i", "n", "t"])`
=> `str().join([chr(112), chr(114), chr(105), chr(110), chr(116)])`
=> `str().join(map(chr, [112, 114, 105, 110, 116]))`
=> `str().join(map(chr, [0x70, 0x72, 0x69, 0x6e, 0x74]))`
"""
from ._str import STR
from .getattr import GETATTR
from .map import MAP
from .chr import CHR

import sys
sys.path.append('..')

from string_factory import make_string

PRINT = f"__builtins__.__getitem__({make_string('print')})"

