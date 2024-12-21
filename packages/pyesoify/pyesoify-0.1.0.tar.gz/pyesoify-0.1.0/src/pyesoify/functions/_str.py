"""
str.py
~~~~~~

This module contains the str function.
`str` can be accessed through `__builtins__.__getitem__("str")`.
So, our task is really to obfuscate `"str"` in the code.

To avoid a "recursive obfuscation"(?) of `str`, we will not use the `str` function to obfuscate `str`.
Since `str` is just 3 letters, and I can't use `str` already, we'll manually `+` the characters.
Thus, we need `'s' + 't' + 'r'`

=> `'s' + 't' + 'r'`
=> `chr(115) + chr(116) + chr(114)`
=> `chr(0x73) + chr(0x74) + chr(0x72)`
=> `chr(0x73).__add__(chr(0x74)).__add__(chr(0x72))`

Let a = 0x73 (115)

=> `chr(a).__add__(chr(a + 1)).__add__(chr(a - 1))`
=> `chr(a).__add__(chr(a.__add__(1))).__add__(chr(a.__sub__(1)))`

Thus, we require `chr`, `a` (115), `1` in this code.
"""
from .chr import CHR
import sys

sys.path.append('..')
from numbers import ONE, HUNDERED_FIFTEEN

STR = f"__builtins__.__getitem__((aae:={HUNDERED_FIFTEEN},{CHR}(aae).__add__({CHR}(aae.__add__({ONE}))).__add__({CHR}(aae.__sub__({ONE})))).__getitem__({ONE}))"

