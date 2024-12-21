import ast
import argparse
from .obfuscate import obfuscate

def get_code(fpath) -> str:
    with open(fpath, "r") as f:
        code = f.read()

    return code

def esoterify(code: str) -> None:
    print('__builtins__: ', end='(')
    for elem in ast.parse(code).body:
        print(obfuscate(elem))

    print(')=__import__("builtins").__dict__')

def main():
    parser = argparse.ArgumentParser(prog="pyesoify", description="Esoterify Python code")
    parser.add_argument("fpath", type=str, help="Path to the Python file to esoterify")
    args = parser.parse_args()

    code = get_code(args.fpath)
    esoterify(code)

