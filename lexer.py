"""
    Python file that contains the function get_tokens(file: Path)
    that extracts tokens from a file and returns a list of tokens along
    with their errors and it's positions.
"""

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

        ############################## Patterns ##############################
        identifier_pattern = re.compile(r"^[a-zA-Z_][a-zA-Z0-9_]*$")
        reserved_words_pattern = re.compile(
            r"\b(if|else|do|while|switch|case|double|main|cin|cout|int|real|then|end|until)\b"
        )
        number_pattern = re.compile(r"\b\d+\b")
        symbol_pattern = re.compile(r"\(|\)|,|{|}|;")
        assignment_pattern = re.compile(r"=")
        logical_op_pattern = re.compile(r"\b(?:and|or)\b")
        ######################################################################

        for index, line in enumerate(f.readlines()):

            col = 1  # Column number always reset to 1 at the beginning of a line
            ln = index + 1  # Line number in the file

            skip_col = 0  # Columns to skip for multiple character tokens

            # Iterate over characters in the line
            for index_string, char in enumerate(line):
                if skip_col == 0:
                    if char == " ":
                        col += 1
                        continue

                    if char == "\t":
                        col += 4
                        continue

                    if char == "\n":
                        continue

                    if re.match(symbol_pattern, char):
                        tokens.append({"Symbol": char})
                        position.append({"Line": ln, "Column": col})
                        col += 1
                        continue

                    if re.match(assignment_pattern, char):
                        if line[index_string + 1] == "=":
                            tokens.append({"Logical Operator": "=="})
                            position.append({"Line": ln, "Column": col})
                            skip_col += 1
                            col += skip_col + 1
                            continue

                        tokens.append({"Assignment": char})
                        position.append({"Line": ln, "Column": col})
                        col += 1
                        continue

                    if re.match(
                        identifier_pattern, char
                    ):  # Check if it is an identifier, a reserved word or a logical operator
                        identifier = ""
                        identifier += char  # Add the first character to the identifier
                        rest_of_string = line[
                            index_string + 1 :
                        ]  # Get the rest of the string

                        while True:
                            for c in rest_of_string:
                                if re.match(identifier_pattern, c):
                                    identifier += c
                                    skip_col += 1
                                else:
                                    break
                            break

                        if re.match(logical_op_pattern, identifier):
                            tokens.append({"Logical Operator": identifier})
                            position.append({"Line": ln, "Column": col})
                            col += skip_col + 1
                            continue

                        if re.match(reserved_words_pattern, identifier):
                            tokens.append({"Reserved Word": identifier})
                            position.append({"Line": ln, "Column": col})
                            col += skip_col + 1
                            continue

                        tokens.append({"Identifier": identifier})
                        position.append({"Line": ln, "Column": col})
                        col += skip_col + 1
                        continue

                    if re.match(number_pattern, char):
                        number = ""
                        number += char
                        rest_of_string = line[index_string + 1 :]
                        is_float_recognized = False

                        while True:
                            for i_c, c in enumerate(rest_of_string):
                                if re.match(number_pattern, c):
                                    number += c
                                    skip_col += 1
                                elif (
                                    c == "."
                                    and re.match(
                                        number_pattern, rest_of_string[i_c + 1]
                                    )
                                    and not is_float_recognized
                                ):
                                    is_float_recognized = True
                                    number += c
                                    skip_col += 1
                                else:
                                    break
                            break

                        if is_float_recognized:
                            tokens.append({"Real Number": number})
                            position.append({"Line": ln, "Column": col})
                            col += skip_col + 1
                            continue

                        tokens.append({"Integer Number": number})
                        position.append({"Line": ln, "Column": col})
                        col += skip_col + 1
                        continue

                    errors.append({"Error": char, "Line": ln, "Column": col})
                    col += 1
                else:
                    skip_col -= 1

        return [errors, position]


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

            for i, element in enumerate(results[0]):
                print(f"{element} at {results[1][i]}")
