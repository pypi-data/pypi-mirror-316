import ast

from pyesoify.obfuscate import obfuscate


def esoterify(code: str, output: str | None) -> None:
    write_buffer = open(output, 'w') if output else None

    print('__builtins__:', end='(', file=write_buffer)
    for elem in ast.parse(code).body:
        print(obfuscate(elem), end='', file=write_buffer)

    print(')=__import__("builtins").__dict__', file=write_buffer)
