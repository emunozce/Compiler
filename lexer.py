import sys
from pathlib import Path


def get_tokens(file: Path):
    tokens = []

    with open(file, "r", encoding="utf-8") as f:
        col = 1
        ln = 1

        for line in f:
            col = 1
            for char in line:
                if char == " ":
                    col += 1
                    continue
                if char == "\t":
                    col += 4
                    continue
                if char == "\n":
                    ln += 1
                    continue
                print(f"{char} Ln: {ln}, Col: {col}")
                col += 1


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
