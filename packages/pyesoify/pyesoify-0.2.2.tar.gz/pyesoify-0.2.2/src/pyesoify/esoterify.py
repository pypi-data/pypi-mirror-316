import ast
import io

from pyesoify.obfuscate import obfuscate


def esoterify(code: str, output: io.TextIOWrapper | None) -> None:
    print('__builtins__:', end='(', file=output)
    for elem in ast.parse(code).body:
        print(obfuscate(elem), end='', file=output)

    print(')=__import__("builtins").__dict__', file=output)
