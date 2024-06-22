from pathlib import Path
import sys
from anytree import Node, RenderTree


class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0
        self.current_token = self.tokens[self.pos] if self.tokens else None

    def parse(self):
        return self.expression()

    def eat(self, token_type):
        if self.current_token and self.current_token.type == token_type:
            self.pos += 1
            self.current_token = (
                self.tokens[self.pos] if self.pos < len(self.tokens) else None
            )
        else:
            raise Exception(
                f"Expected token {token_type}, got {self.current_token.type}"
            )

    def expression(self):
        node = self.term()
        while (
            self.current_token
            and self.current_token.type == "ARITHMETIC_OPERATOR"
            and self.current_token.value in ("+", "-")
        ):
            token = self.current_token
            self.eat("ARITHMETIC_OPERATOR")
            node = Node(token.value, children=[node, self.term()])
        return node

    def term(self):
        node = self.factor()
        while (
            self.current_token
            and self.current_token.type == "ARITHMETIC_OPERATOR"
            and self.current_token.value in ("*", "/", "%")
        ):
            token = self.current_token
            self.eat("ARITHMETIC_OPERATOR")
            node = Node(token.value, children=[node, self.factor()])
        return node

    def factor(self):
        node = self.base()
        while (
            self.current_token
            and self.current_token.type == "ARITHMETIC_OPERATOR"
            and self.current_token.value == "^"
        ):
            token = self.current_token
            self.eat("ARITHMETIC_OPERATOR")
            node = Node(token.value, children=[node, self.base()])
        return node

    def base(self):
        token = self.current_token
        if token.type in (
            "INTEGER_NUMBER",
            "REAL_NUMBER",
            "NEGATIVE_INTEGER_NUMBER",
            "NEGATIVE_REAL_NUMBER",
        ):
            self.eat(token.type)
            return Node(token.value)
        elif token.type == "LPAREN":
            self.eat("LPAREN")
            node = self.expression()
            self.eat("RPAREN")
            return node
        elif token.type == "IDENTIFIER":
            self.eat("IDENTIFIER")
            return Node(token.value)
        else:
            raise Exception(f"Unexpected token {token.type}")

    def render_tree(self, node):
        return "\n".join([f"{pre}{node.name}" for pre, fill, node in RenderTree(node)])


# Example usage
if __name__ == "__main__":
    from anytree.exporter import DotExporter
    from lexer import get_lexical_analysis

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
            # bytes = file_path.read_bytes()
            # print(bytes)
            tkns, errs = get_lexical_analysis(file_path)

            parser = Parser(tkns)
            ast = parser.parse()

            # Render the tree as a string
            tree_str = parser.render_tree(ast)

            print(tree_str)

            # Optionally, export the tree to a file (e.g., a dot file for visualization)
            DotExporter(ast).to_dotfile("ast.dot")
