import ast
from typing import Any

from pyesoify import string_factory
from pyesoify import numbers
from pyesoify import operators
from pyesoify import functions

def obfs_type(value: Any) -> str:
    if isinstance(value, str):
        return string_factory.make_string(value)
    if isinstance(value, int):
        return numbers.obfs_number(value)
    return str(value)

def obfs_name(name: str) -> str:
    return name + str(abs(hash(name)))

def obfuscate(elem):
    if isinstance(elem, ast.Expr):
        return obfuscate(elem.value)
    elif isinstance(elem, ast.Assign):
        return f'{obfuscate(elem.targets[0])}:=({obfuscate(elem.value)}),'
    elif isinstance(elem, ast.BinOp):
        return f"{obfuscate(elem.left)}.{operators.obfs_operator(elem.op)}({obfuscate(elem.right)})" 
    elif isinstance(elem, ast.Constant):
        return obfs_type(elem.value)
    elif isinstance(elem, ast.Name):
        return obfs_name(elem.id)
    elif isinstance(elem, ast.Call) \
        and isinstance(elem.func, ast.Name) \
        and isinstance(elem.func.ctx, ast.Load):
        params = map(lambda arg: obfuscate(arg), elem.args)

        return f'{functions.obfs_function(elem.func.id)}({",".join(params)})'
    return ''
