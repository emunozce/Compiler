import sys
from pathlib import Path


def get_tokens(file):
    with open(file, "r", encoding="utf-8") as f:
        for line in f:
            print(line)


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
