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

        # Flag to check if the current character is inside a block comment
        is_block_comment = False

        # Store the position of the block comment starting Ln and Col
        is_block_starting = []

        ############################## Patterns ##############################
        identifier_pattern = re.compile(r"^[a-zA-Z_][a-zA-Z0-9_]*$")
        reserved_words_pattern = re.compile(
            r"\b(if|else|do|while|switch|case|double|main|cin|cout|int|real|then|end|until)\b"
        )
        number_pattern = re.compile(r"\b\d+\b")
        symbol_pattern = re.compile(r"\(|\)|,|{|}|;")
        assignment_pattern = re.compile(r"=")
        logical_op_pattern = re.compile(r"\b(?:and|or)\b")
        aritmethic_op_pattern = re.compile(r"\+|-|\*|/|%|\^")
        relational_op_pattern = re.compile(r"<|>|!")
        ######################################################################

        for index, line in enumerate(f.readlines()):

            skip_col = 0  # Columns to skip for multiple character tokens

            # Iterate over characters in the line
            for index_string, char in enumerate(line):
                if skip_col == 0:
                    if char == " ":
                        continue

                    if char == "\t":
                        continue

                    if char == "\n":
                        continue

                    if re.match(symbol_pattern, char) and (not is_block_comment):
                        tokens.append({"Symbol": char})
                        continue

                    if re.match(assignment_pattern, char) and (not is_block_comment):
                        if (index_string + 1 < len(line)) and line[
                            index_string + 1
                        ] == "=":
                            tokens.append({"Logical Operator": "=="})
                            skip_col += 1
                            continue

                        tokens.append({"Assignment": char})
                        continue

                    if re.match(aritmethic_op_pattern, char) and (not is_block_comment):
                        if char == "+" and line[index_string + 1] == "+":
                            tokens.append({"Increment Operator": "++"})
                            skip_col += 1
                            continue

                        if char == "-" and line[index_string + 1] == "-":
                            tokens.append({"Decrement Operator": "--"})
                            skip_col += 1
                            continue

                        if (
                            char == "/"
                            and (index_string + 1 < len(line))
                            and (
                                line[index_string + 1] == "*"
                                or (line[index_string + 1] == "/")
                            )
                        ):
                            is_block_starting = [index + 1, index_string + 1]
                            is_block_comment = True
                            break

                        tokens.append({"Arithmetic Operator": char})
                        continue

                    if re.match(relational_op_pattern, char) and (not is_block_comment):
                        if (index_string + 1 < len(line)) and line[
                            index_string + 1
                        ] == "=":
                            tokens.append({"Relational Operator": char + "="})
                            skip_col += 1
                            continue
                        tokens.append({"Relational Operator": char})
                        continue

                    if re.match(identifier_pattern, char) and (
                        not is_block_comment
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
                            continue

                        if re.match(reserved_words_pattern, identifier):
                            tokens.append({"Reserved Word": identifier})
                            continue

                        tokens.append({"Identifier": identifier})
                        continue

                    if re.match(number_pattern, char) and (not is_block_comment):
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
                            continue

                        tokens.append({"Integer Number": number})
                        continue

                    if not is_block_comment:
                        errors.append(
                            {
                                "Error": char,
                                "Ln": index + 1,
                                "Col": index_string + 1,
                            }
                        )

                    if is_block_comment:
                        if (
                            char == "*"
                            and (index_string + 1 < len(line))
                            and line[index_string + 1] == "/"
                        ):
                            is_block_comment = False
                            skip_col += 1
                else:
                    skip_col -= 1

        if is_block_comment:
            errors.append(
                {
                    "Error": f"Block comment not closed at Ln: {is_block_starting[0]}, Col {is_block_starting[1]}"
                }
            )

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

            for element in results[0]:
                print(f"{element}")

            for element in results[1]:
                print(f"{element}")
