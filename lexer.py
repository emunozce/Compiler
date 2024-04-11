import sys
from pathlib import Path
import re
from unittest import skip


def get_tokens(file: Path):

    with open(file, "r", encoding="utf-8") as f:
        tokens = []  # Store the token
        position = []  # Store the position of the token in the file

        identifier_pattern = re.compile(r"^[a-zA-Z_][a-zA-Z0-9_]*$")
        reserved_words_pattern = re.compile(
            r"\b(if|else|do|while|switch|case|integer|double|main|cin|cout)\b"
        )
        number_pattern = re.compile(r"^\d+(\.\d+)?$")
        symbol_pattern = re.compile(r"\(|\)|,|{|}|;")
        assignment_pattern = re.compile(r"=")

        lines = f.readlines()

        for index, line in enumerate(lines):  # Enumerate lines starting from 1
            col = 1  # Column number always reset to 1 at the beginning of a line
            skip_col = 0
            ln = index + 1

            # Iterate over characters in the line
            for char in line:
                if skip_col == 0:
                    if char == " ":
                        col += 1
                        continue
                    if char == "\t":
                        col += 4
                        continue
                    if char == "\n":
                        col = 1
                        continue
                    if re.match(symbol_pattern, char):
                        tokens.append({"Symbol": char})
                        position.append({"Line": ln, "Column": col})
                        col += 1
                        continue

                    if re.match(identifier_pattern, char):
                        identifier = char
                        for char in line[col:]:
                            if re.match(identifier_pattern, char):
                                identifier += char
                                col += 1
                                skip_col += 1
                            else:
                                col += 1
                                break
                        if re.match(reserved_words_pattern, identifier):
                            tokens.append({"Reserved Word": identifier})
                            position.append({"Line": ln, "Column": col})
                        else:
                            tokens.append({"Identifier": identifier})
                            position.append({"Line": ln, "Column": col})

                        continue

                    if re.match(assignment_pattern, char):
                        if line[col] == "=":
                            tokens.append({"Relational Operator": "=="})
                            position.append({"Line": ln, "Column": col})
                            col += 1
                            skip_col += 1  # Skip the next character
                        else:
                            tokens.append({"Assignment Operator": "="})
                            position.append({"Line": ln, "Column": col})
                            col += 1
                else:
                    col += 1
                    skip_col -= 1

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
