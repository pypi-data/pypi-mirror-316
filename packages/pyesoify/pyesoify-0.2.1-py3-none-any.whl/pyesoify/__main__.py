import ast
import argparse
from pyesoify.obfuscate import obfuscate

def get_code(fpath) -> str:
    with open(fpath, "r") as f:
        code = f.read()

    return code

def esoterify(code: str, output: str) -> None:
    import sys
    if output:
        sys.stdout = open(output, 'w')

    print('__builtins__:', end='(')
    for elem in ast.parse(code).body:
        print(obfuscate(elem), end='')

    print(')=__import__("builtins").__dict__')

def main():
    parser = argparse.ArgumentParser(prog="pyesoify", description="Esoterify Python code")
    parser.add_argument("fpath", type=str, help="Path to the Python file to esoterify")
    parser.add_argument("--output", type=str, help="Path to the output file", default='')

    args = parser.parse_args()

    code = get_code(args.fpath)
    esoterify(code, output=args.output)

if __name__ == "__main__":
    main()

