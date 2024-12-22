"""
chr.py
~~~~~~

This module contains the chr function.
`chr` can be accessed through `__builtins__.__getitem__("chr")`.

So, our task is really to obfuscate `"chr"` in the code.
`__builtins__` contains all the built-in functions.

We can get the chr function through:
`__builtins__["chr"]`, but this requires `"chr"` and that's annoying.
So, we get an iterator, convert to list, index to get `chr`

`__builtins__.__iter__()`
=> `[*__builtins__.__iter__()]`

Element at index 14 is `chr`, so we can get `chr` through:
`[*__builtins__.__iter__()][14]`

So, we only require `14` in the code.
"""
from pyesoify.numbers import FOURTEEN

CHR = f"__builtins__.__getitem__([*__builtins__.__iter__()].__getitem__({FOURTEEN}))"
