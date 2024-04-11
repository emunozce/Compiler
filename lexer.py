import sys
from pathlib import Path


def get_tokens(file: Path):
    tokens = []
    lin = 1
    column = 1

    with open(file, "r", encoding="utf-8") as f:
        for line in f:
            lin = 1
            for char in line:
                if char == " ":
                    lin += 1
                    continue
                elif char == "\t":
                    lin += 4
                    continue
                elif char == "\n":
                    column += 1
                    continue
                print(f"{char} line: {lin} column: {column}")
                lin += 1


if __name__ == "__main__":
    args = sys.argv
    if len(args) < 2:
        print("No arguments provided")
    elif len(args) > 2:
        print("Bad arguments")
    else:
        file_path = Path(args[1])
        if not file_path.exists():
            print("File does not exist")
        else:
            get_tokens(file_path)
