import sys
from pathlib import Path
import re


def get_tokens(file: Path):

    with open(file, "r", encoding="utf-8") as f:
        tokens = []  # Store the token
        position = []  # Store the position of the token in the file

        identifier_pattern = re.compile(r"^[a-zA-Z_][a-zA-Z0-9_]*$")
        number_pattern = re.compile(r"^\d+(\.\d+)?$")
        symbol_pattern = re.compile(r"\(|\)|,|{|}|;")
        assignment_pattern = re.compile(r"=")

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
                if re.match(symbol_pattern, char):
                    tokens.append({"Symbol": char})
                    position.append({"Line": ln, "Column": col})
                    col += 1
                    continue
                if re.match(assignment_pattern, char):
                    tokens.append({"Assignment": char})
                    position.append({"Line": ln, "Column": col})
                    col += 1
                    continue
                col += 1

        for i, token in enumerate(tokens):
            print(f"{token} {position[i]}\n")


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
