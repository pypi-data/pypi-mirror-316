import argparse
import ast

from pyesoify.esoterify import esoterify


def get_code(fpath) -> str:
    with open(fpath, "r") as f:
        code = f.read()

    return code

def main():
    parser = argparse.ArgumentParser(prog="pyesoify", description="Esoterify Python code")
    parser.add_argument("fpath", type=str, help="Path to the Python file to esoterify")
    parser.add_argument("--output", type=str, help="Path to the output file", default=None)

    args = parser.parse_args()

    code = get_code(args.fpath)
    esoterify(code, output=args.output)

if __name__ == "__main__":
    main()
