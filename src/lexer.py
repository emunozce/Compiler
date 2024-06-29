"""
    Python file that contains the function get_tokens(file: Path)
    that extracts tokens from a file and returns a list of tokens along
    with their errors and it's positions.
"""

from pathlib import Path
import re


class Token:
    def __init__(self, type, value, lineno, lexpos):
        self.type = type
        self.value = value
        self.lineno = lineno
        self.lexpos = lexpos

    def __repr__(self):
        return f"({self.type}, {self.value}, {self.lineno}, {self.lexpos})"


def get_lexical_analysis(file: Path):
    with open(file, "r", encoding="utf-8") as f:
        tokens = []
        errors = []
        is_block_comment = False
        is_block_starting = []
        identifier_pattern = re.compile(r"^[a-zA-Z_][a-zA-Z0-9_]*$")
        reserved_words_pattern = re.compile(
            r"\b(if|else|do|while|switch|case|double|main|cin|cout|int|float)\b"
        )
        number_pattern = re.compile(r"\b\d+\b")
        symbol_pattern = re.compile(r"\(|\)|,|{|}|;")
        assignment_pattern = re.compile(r"=")
        logical_op_pattern = re.compile(r"\b(?:and|or)\b")
        aritmethic_op_pattern = re.compile(r"\+|-|\*|/|%|\^")
        relational_op_pattern = re.compile(r"<|>|!")

        for lineno, line in enumerate(f.readlines(), start=1):
            skip_col = 0
            for index_string, char in enumerate(line):
                lexpos = index_string + 1
                if skip_col == 0:
                    if char == " ":
                        continue
                    if char == "\t":
                        continue
                    if char == "\n":
                        continue

                    if re.match(symbol_pattern, char) and not is_block_comment:
                        identify_symbol(char, tokens, lineno, lexpos)
                        continue

                    if re.match(assignment_pattern, char) and not is_block_comment:
                        if (index_string + 1 < len(line)) and line[
                            index_string + 1
                        ] == "=":
                            tokens.append(Token("EQ", "==", lineno, lexpos))
                            skip_col += 1
                            continue
                        tokens.append(Token("ASSIGN", char, lineno, lexpos))
                        continue

                    if re.match(aritmethic_op_pattern, char) and not is_block_comment:
                        if char == "+" and line[index_string + 1] == "+":
                            tokens.append(
                                Token("INCREMENT_OPERATOR", "++", lineno, lexpos)
                            )
                            skip_col += 1
                            continue
                        if char == "-" and line[index_string + 1] == "-":
                            tokens.append(
                                Token("DECREMENT_OPERATOR", "--", lineno, lexpos)
                            )
                            skip_col += 1
                            continue
                        if (
                            char == "/"
                            and (index_string + 1 < len(line))
                            and (line[index_string + 1] == "*")
                        ):
                            is_block_starting = [lineno, lexpos]
                            is_block_comment = True
                            break
                        if (
                            char == "/"
                            and (index_string + 1 < len(line))
                            and line[index_string + 1] == "/"
                        ):
                            break
                        identify_aritmethic_operator(char, tokens, lineno, lexpos)
                        continue

                    if re.match(relational_op_pattern, char) and not is_block_comment:
                        if (index_string + 1 < len(line)) and line[
                            index_string + 1
                        ] == "=":
                            identify_relational_operator(
                                char + "=", tokens, lineno, lexpos
                            )
                            skip_col += 1
                            continue
                        identify_relational_operator(char, tokens, lineno, lexpos)
                        continue

                    if re.match(identifier_pattern, char) and not is_block_comment:
                        identifier = char
                        rest_of_string = line[index_string + 1 :]
                        while True:
                            for c in rest_of_string:
                                if re.match(identifier_pattern, (identifier + c)):
                                    identifier += c
                                    skip_col += 1
                                else:
                                    break
                            break

                        if re.match(logical_op_pattern, identifier):
                            identify_logical_operator(
                                identifier, tokens, lineno, lexpos
                            )
                            continue

                        if re.match(reserved_words_pattern, identifier):
                            identify_reserved_words(identifier, tokens, lineno, lexpos)
                            continue

                        tokens.append(Token("IDENTIFIER", identifier, lineno, lexpos))
                        continue

                    if re.match(number_pattern, char) and not is_block_comment:
                        number = char
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
                            if tokens and tokens[-1].value == "-":
                                if (
                                    len(tokens) >= 2
                                    and tokens[-2].value == "("
                                    or tokens[-2].type
                                    not in (
                                        "INTEGER_NUMBER",
                                        "REAL_NUMBER",
                                        "NEGATIVE_INTEGER_NUMBER",
                                        "NEGATIVE_REAL_NUMBER",
                                    )
                                ):
                                    tokens.pop()
                                    number = "-" + number
                                    tokens.append(
                                        Token(
                                            "NEGATIVE_REAL_NUMBER",
                                            number,
                                            lineno,
                                            lexpos,
                                        )
                                    )
                                    continue
                            tokens.append(Token("REAL_NUMBER", number, lineno, lexpos))
                            continue
                        if tokens and tokens[-1].value == "-":
                            if tokens and tokens[-1].value == "-":
                                if (
                                    len(tokens) >= 2
                                    and tokens[-2].value == "("
                                    or tokens[-2].type
                                    not in (
                                        "INTEGER_NUMBER",
                                        "REAL_NUMBER",
                                        "NEGATIVE_INTEGER_NUMBER",
                                        "NEGATIVE_REAL_NUMBER",
                                    )
                                ):
                                    tokens.pop()
                                    number = "-" + number
                                    tokens.append(
                                        Token(
                                            "NEGATIVE_INTEGER_NUMBER",
                                            number,
                                            lineno,
                                            lexpos,
                                        )
                                    )
                                    continue
                        tokens.append(Token("INTEGER_NUMBER", number, lineno, lexpos))
                        continue

                    if not is_block_comment:
                        errors.append(
                            Token(
                                "ERROR",
                                f"Invalid character => {char}",
                                lineno,
                                lexpos,
                            )
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
                Token(
                    "ERROR",
                    "Block comment not closed",
                    is_block_starting[0],
                    is_block_starting[1],
                )
            )

        return tokens, errors


def identify_symbol(char: str, tokens: list, lineno: int, lexpos: int):
    if char == "(":
        tokens.append(Token("LPAREN", char, lineno, lexpos))
    if char == ")":
        tokens.append(Token("RPAREN", char, lineno, lexpos))
    if char == ",":
        tokens.append(Token("COMMA", char, lineno, lexpos))
    if char == "{":
        tokens.append(Token("LBRACE", char, lineno, lexpos))
    if char == "}":
        tokens.append(Token("RBRACE", char, lineno, lexpos))
    if char == ";":
        tokens.append(Token("SEMICOLON", char, lineno, lexpos))


def identify_aritmethic_operator(char: str, tokens: list, lineno: int, lexpos: int):
    if char == "+":
        tokens.append(Token("PLUS", char, lineno, lexpos))
    if char == "-":
        tokens.append(Token("MINUS", char, lineno, lexpos))
    if char == "*":
        tokens.append(Token("TIMES", char, lineno, lexpos))
    if char == "/":
        tokens.append(Token("DIVIDE", char, lineno, lexpos))
    if char == "%":
        tokens.append(Token("MOD", char, lineno, lexpos))
    if char == "^":
        tokens.append(Token("POW", char, lineno, lexpos))


def identify_relational_operator(char: str, tokens: list, lineno: int, lexpos: int):
    if char == "<":
        tokens.append(Token("LT", char, lineno, lexpos))
    if char == ">":
        tokens.append(Token("GT", char, lineno, lexpos))
    if char == "!":
        tokens.append(Token("NOT", char, lineno, lexpos))
    if char == "<=":
        tokens.append(Token("LE", char, lineno, lexpos))
    if char == ">=":
        tokens.append(Token("GE", char, lineno, lexpos))
    if char == "!=":
        tokens.append(Token("NE", char, lineno, lexpos))


def identify_logical_operator(char: str, tokens: list, lineno: int, lexpos: int):
    if char == "and":
        tokens.append(Token("AND", char, lineno, lexpos))
    if char == "or":
        tokens.append(Token("OR", char, lineno, lexpos))


def identify_reserved_words(char: str, tokens: list, lineno: int, lexpos: int):
    if char == "if":
        tokens.append(Token("IF", char, lineno, lexpos))
    if char == "else":
        tokens.append(Token("ELSE", char, lineno, lexpos))
    if char == "do":
        tokens.append(Token("DO", char, lineno, lexpos))
    if char == "while":
        tokens.append(Token("WHILE", char, lineno, lexpos))
    if char == "switch":
        tokens.append(Token("SWITCH", char, lineno, lexpos))
    if char == "case":
        tokens.append(Token("CASE", char, lineno, lexpos))
    if char == "double":
        tokens.append(Token("DOUBLE", char, lineno, lexpos))
    if char == "main":
        tokens.append(Token("MAIN", char, lineno, lexpos))
    if char == "cin":
        tokens.append(Token("CIN", char, lineno, lexpos))
    if char == "cout":
        tokens.append(Token("COUT", char, lineno, lexpos))
    if char == "int":
        tokens.append(Token("INT", char, lineno, lexpos))
    if char == "float":
        tokens.append(Token("FLOAT", char, lineno, lexpos))


if __name__ == "__main__":
    import sys

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
            tkns, errs = get_lexical_analysis(file_path)

            for token in tkns:
                print(f"{token}")

            for error in errs:
                print(f"{error}")
