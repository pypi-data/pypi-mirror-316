"""
getattr.py
~~~~~~~~~~

This module contains the getattribute function.
`getattribute` can be accessed through `__builtins__.__getitem__("getattr")`.
"""
from pyesoify.numbers import FOURTEEN, HUNDERED

GETATTR = f"__builtins__.__getitem__([*__builtins__.__iter__()].__getitem__({FOURTEEN}.__add__({HUNDERED})))"
