import re
from anytree import Node, RenderTree, AsciiStyle

# Tokenizer
token_pattern = re.compile(r"\s*(?:(\d+|\+|\-|\*|\/|\%|\^|\(|\)))\s*")


def tokenize(expression):
    tokens = token_pattern.findall(expression)
    return [token for token in tokens if token]


# Parser functions with error handling
def parse_expression(tokens, parent=None):
    if not tokens:
        raise ValueError("Unexpected end of expression")
    node, tokens = parse_term(tokens, parent)
    while tokens and tokens[0] in ("+", "-"):
        op = tokens.pop(0)
        operator_node = Node(op, parent)
        right_node, tokens = parse_term(tokens, operator_node)
        node.parent = operator_node
        operator_node.children = [node, right_node]
        node = operator_node
    return node, tokens


def parse_term(tokens, parent=None):
    if not tokens:
        raise ValueError("Unexpected end of term")
    node, tokens = parse_factor(tokens, parent)
    while tokens and tokens[0] in ("*", "/", "%"):
        op = tokens.pop(0)
        operator_node = Node(op, parent)
        right_node, tokens = parse_factor(tokens, operator_node)
        node.parent = operator_node
        operator_node.children = [node, right_node]
        node = operator_node
    return node, tokens


def parse_factor(tokens, parent=None):
    if not tokens:
        raise ValueError("Unexpected end of factor")
    node, tokens = parse_primary(tokens, parent)
    while tokens and tokens[0] == "^":
        op = tokens.pop(0)
        operator_node = Node(op, parent)
        right_node, tokens = parse_primary(tokens, operator_node)
        node.parent = operator_node
        operator_node.children = [node, right_node]
        node = operator_node
    return node, tokens


def parse_primary(tokens, parent=None):
    if not tokens:
        raise ValueError("Unexpected end of primary")
    token = tokens.pop(0)
    if token == "(":
        node, tokens = parse_expression(tokens, parent)
        if not tokens or tokens[0] != ")":
            raise ValueError("Mismatched parentheses")
        tokens.pop(0)  # remove ')'
        return node, tokens
    elif token.isdigit():
        return Node(token, parent), tokens
    else:
        raise ValueError(f"Unexpected token: {token}")


# Main function to parse an expression and return the parse tree
def parse(expression):
    tokens = tokenize(expression)
    try:
        tree, tokens = parse_expression(tokens)
        if tokens:
            raise ValueError(f"Unexpected tokens remaining: {tokens}")
        return tree
    except ValueError as e:
        print(f"Error parsing expression: {e}")
        return None


# Example usage
expression = "3 + 5 * (2 - 8) % 2"
tree = parse(expression)
if tree:
    for pre, fill, node in RenderTree(tree, style=AsciiStyle()):
        print("%s%s" % (pre, node.name))

# Error examples
invalid_expression = "3 + 5 * (2 - 8 ^ 2"
parse(invalid_expression)

invalid_expression = "3 + 5 * 2 - 8 ^"
parse(invalid_expression)

invalid_expression = "3 + 5 * 2a - 8"
parse(invalid_expression)
