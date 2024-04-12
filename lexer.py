import sys
from pathlib import Path
import re


def get_tokens(file: Path):

    with open(file, "r", encoding="utf-8") as f:
        tokens = []  # Store the token
        errors = []  # Store the error
        position = []  # Store the position of the token in the file

        identifier_pattern = re.compile(r"^[a-zA-Z_][a-zA-Z0-9_]*$")
        reserved_words_pattern = re.compile(
            r"\b(if|else|do|while|switch|case|integer|double|main|cin|cout)\b"
        )
        number_pattern = re.compile(r"^\d+(\.\d+)?$")
        symbol_pattern = re.compile(r"\(|\)|,|{|}|;")
        assignment_pattern = re.compile(r"=")

        lines = f.readlines()

        for index, string in enumerate(lines):  # Enumerate lines starting from 1
            col = 1  # Column number always reset to 1 at the beginning of a line
            skip_col = 0
            ln = index + 1

            # Iterate over characters in the line
            for char in string:
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
                        identifier = ""
                        identifier += char  # Add the first character to the identifier
                        new_string = string[col:]  # Get the rest of the string

                        i = 0
                        while i < len(new_string) and re.match(
                            identifier_pattern, new_string[i]
                        ):
                            identifier += new_string[i]
                            col += 1
                            skip_col += 1
                            i += 1

                        if re.match(reserved_words_pattern, identifier):
                            tokens.append({"Reserved Word": identifier})
                            position.append(
                                {"Line": ln, "Column": col - len(identifier) + 1}
                            )
                            col += 1
                            continue

                        tokens.append({"Identifier": identifier})
                        position.append(
                            {"Line": ln, "Column": col - len(identifier) + 1}
                        )
                        col += 1
                        continue

                    errors.append({"Error": char, "Line": ln, "Column": col})
                    col += 1
                else:
                    skip_col -= 1

        for i, token in enumerate(tokens):
            print(f"{token} {position[i]}\n")

        # for i, error in enumerate(errors):
        #     print(f"{error}\n")


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
