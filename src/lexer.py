# lexer.py (modificado para imprimir tokens)
import sys
from pathlib import Path
import re

def get_lexycal_analysis(file: Path):
    with open(file, "r", encoding="utf-8") as f:
        tokens = []
        errors = []
        is_block_comment = False
        is_block_starting = []

        identifier_pattern = re.compile(r"^[a-zA-Z_][a-zA-Z0-9_]*$")
        reserved_words_pattern = re.compile(
            r"\b(if|else|do|while|switch|case|double|main|cin|cout|int|real|then|end|until)\b"
        )
        number_pattern = re.compile(r"\b\d+(\.\d+)?\b")
        symbol_pattern = re.compile(r"\(|\)|,|{|}|;")
        assignment_pattern = re.compile(r"=")
        logical_op_pattern = re.compile(r"\b(?:and|or)\b")
        aritmethic_op_pattern = re.compile(r"\+|-|\*|/|%|\^")
        relational_op_pattern = re.compile(r"<|>|!|==|<=|>=|!=")

        for index, line in enumerate(f.readlines()):
            skip_col = 0

            for index_string, char in enumerate(line):
                if skip_col == 0:
                    if char in [" ", "\t", "\n"]:
                        continue

                    if re.match(symbol_pattern, char) and (not is_block_comment):
                        tokens.append({"Symbol": char})
                        continue

                    if re.match(assignment_pattern, char) and (not is_block_comment):
                        if (index_string + 1 < len(line)) and line[index_string + 1] == "=":
                            tokens.append({"Relational Operator": "=="})
                            skip_col += 1
                            continue
                        tokens.append({"Assignment": char})
                        continue

                    if re.match(aritmethic_op_pattern, char) and (not is_block_comment):
                        if char == "+" and (index_string + 1 < len(line)) and line[index_string + 1] == "+":
                            tokens.append({"Increment Operator": "++"})
                            skip_col += 1
                            continue
                        if char == "-" and (index_string + 1 < len(line)) and line[index_string + 1] == "--":
                            tokens.append({"Decrement Operator": "--"})
                            skip_col += 1
                            continue
                        if char == "/" and (index_string + 1 < len(line)) and line[index_string + 1] == "*":
                            is_block_starting = [index + 1, index_string + 1]
                            is_block_comment = True
                            break
                        if char == "/" and (index_string + 1 < len(line)) and line[index_string + 1] == "/":
                            break
                        tokens.append({"Arithmetic Operator": char})
                        continue

                    if re.match(relational_op_pattern, char) and (not is_block_comment):
                        if (index_string + 1 < len(line)) and line[index_string + 1] == "=":
                            tokens.append({"Relational Operator": char + "="})
                            skip_col += 1
                            continue
                        tokens.append({"Relational Operator": char})
                        continue

                    if re.match(identifier_pattern, char) and (not is_block_comment):
                        identifier = ""
                        identifier += char
                        rest_of_string = line[index_string + 1:]

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
                        rest_of_string = line[index_string + 1:]
                        is_float_recognized = False

                        while True:
                            for i_c, c in enumerate(rest_of_string):
                                if re.match(number_pattern, c):
                                    number += c
                                    skip_col += 1
                                elif c == "." and re.match(number_pattern, rest_of_string[i_c + 1]) and not is_float_recognized:
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
                        errors.append({"Error": char, "Ln": index + 1, "Col": index_string + 1})

                    if is_block_comment:
                        if char == "*" and (index_string + 1 < len(line)) and line[index_string + 1] == "/":
                            is_block_comment = False
                            skip_col += 1
                else:
                    skip_col -= 1

        if is_block_comment:
            errors.append({"Error": f"Block comment not closed at Ln: {is_block_starting[0]}, Col {is_block_starting[1]}"})

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
            tkns, errs = get_lexycal_analysis(file_path)

            for token in tkns:
                print(f"{token}")

            for error in errs:
                print(f"{error}")
