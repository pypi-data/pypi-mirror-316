import ast
from .obfuscate import obfuscate

def get_code(fpath="examples/code.py") -> str:
    with open(fpath, "r") as f:
        code = f.read()

    return code

def main(code: str) -> None:
    print('__builtins__: ', end='(')
    for elem in ast.parse(code).body:
        print(obfuscate(elem))

    print(')=__import__("builtins").__dict__')

