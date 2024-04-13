import sys
from pathlib import Path
import re


def get_tokens(file: Path):
    """
    Extracts tokens from a file and returns a list of tokens along with their positions.

    Args:
        file (Path): The path to the file to be processed.

    Returns:
        list: A list containing in [0] a list of dictionaries representing tokens
        containing the token type and in [1] a list of dictionaries
        representing errors and its position in the file.

    Raises:
        None

    """
    with open(file, "r", encoding="utf-8") as f:
        tokens = []  # Store the tokens found
        errors = []  # Store the errors
        position = []  # Store the position of the token in the file

        identifier_pattern = re.compile(r"^[a-zA-Z_][a-zA-Z0-9_]*$")
        reserved_words_pattern = re.compile(
            r"\b(if|else|do|while|switch|case|double|main|cin|cout|int|real|then|end|until)\b"
        )
        number_pattern = re.compile(r"\b\d+\b")
        symbol_pattern = re.compile(r"\(|\)|,|{|}|;")
        assignment_pattern = re.compile(r"=")
        logical_op_pattern = re.compile(r"\b(?:and|or)\b")

        lines = f.readlines()

        for index, string in enumerate(lines):  # Enumerate lines starting from 1
            col = 1  # Column number always reset to 1 at the beginning of a line
            skip_col = 0
            ln = index + 1

            # Iterate over characters in the line
            for index_string, char in enumerate(string):
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

                    if re.match(assignment_pattern, char):
                        if string[index_string + 1] == "=":
                            tokens.append({"Logical Operator": "=="})
                            position.append({"Line": ln, "Column": col})
                            col += 2
                            skip_col += 1
                            continue

                        tokens.append({"Assignment": char})
                        position.append({"Line": ln, "Column": col})
                        col += 1
                        continue

                    if re.match(number_pattern, char):
                        number = ""
                        number += char  # Add the first character to the number
                        new_string = string[col:]  # Get the rest of the string

                        i = 0
                        while i < len(new_string) and re.match(
                            number_pattern, new_string[i]
                        ):
                            number += new_string[i]
                            col += 1
                            skip_col += 1
                            i += 1

                        if (
                            i < len(new_string)
                            and new_string[i] == "."
                            and re.match(number_pattern, new_string[i + 1])
                        ):
                            number += new_string[i]
                            col += 2
                            skip_col += 1
                            i += 1
                            while i < len(new_string) and re.match(
                                number_pattern, new_string[i]
                            ):
                                number += new_string[i]
                                col += 1
                                skip_col += 1
                                i += 1
                            tokens.append({"Float Number": number})
                            continue
                        elif i < len(new_string) and new_string[i] != ".":
                            tokens.append({"Integer Number": number})
                            col += 1
                            continue
                        errors.append({"Error": char, "Line": ln, "Column": col})
                        col += 1
                        continue

                    if re.match(
                        identifier_pattern, char
                    ):  # Check if it is an identifier, a reserved word or a logical operator
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

                        if re.match(logical_op_pattern, identifier):
                            tokens.append({"Logical Operator": identifier})
                            position.append(
                                {"Line": ln, "Column": col - len(identifier) + 1}
                            )
                            col += 1
                            continue

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

        return [tokens, errors]


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
            results = get_tokens(file_path)
            int_numbers = [num for num in results[0] if "Integer Number" in num]
            float_numbers = [num for num in results[0] if "Float Number" in num]

            # for token in numbers:
            #     print(f"{token}")

            for token in results[0]:
                print(f"{token}")

            for token in results[1]:
                print(f"{token}")
