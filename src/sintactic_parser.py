from anytree import Node, RenderTree


class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.current_token = None
        self.next_token()

    def next_token(self):
        self.current_token = self.tokens.pop(0) if self.tokens else None

    def parse(self):
        return self.exp()

    def exp(self):
        node = self.term()
        while (
            self.current_token
            and self.current_token["Token Type"] == "operator"
            and self.current_token["Value"] in ("+", "-")
        ):
            op = Node(self.current_token["Value"])
            self.next_token()
            op.children = [node, self.term()]
            node = op
        return node

    def term(self):
        node = self.fac()
        while (
            self.current_token
            and self.current_token["Token Type"] == "operator"
            and self.current_token["Value"] in ("*", "/")
        ):
            op = Node(self.current_token["Value"])
            self.next_token()
            op.children = [node, self.fac()]
            node = op
        return node

    def fac(self):
        if (
            self.current_token["Token Type"] == "paren"
            and self.current_token["Value"] == "("
        ):
            self.next_token()
            node = self.exp()
            if (
                self.current_token["Token Type"] == "paren"
                and self.current_token["Value"] == ")"
            ):
                self.next_token()
            return node
        elif self.current_token["Token Type"] in [
            "integer number",
            "floating point number",
            "identifier",
        ]:
            node = Node(self.current_token["Value"])
            self.next_token()
            return node
        else:
            raise SyntaxError("Unexpected token")


def main():
    tokens_list = [
        [
            {"Token Type": "integer number", "Value": "3"},
            {"Token Type": "operator", "Value": "+"},
            {"Token Type": "integer number", "Value": "5"},
            {"Token Type": "operator", "Value": "*"},
            {"Token Type": "paren", "Value": "("},
            {"Token Type": "integer number", "Value": "2"},
            {"Token Type": "operator", "Value": "-"},
            {"Token Type": "integer number", "Value": "8"},
            {"Token Type": "paren", "Value": ")"},
        ],
        [
            {"integer number": "10"},
            {"operator": "+"},
            {"integer number": "2"},
            {"operator": "*"},
            {"integer number": "6"},
        ],
        [
            {"Token Type": "integer number", "Value": "100"},
            {"Token Type": "operator", "Value": "*"},
            {"Token Type": "paren", "Value": "("},
            {"Token Type": "integer number", "Value": "2"},
            {"Token Type": "operator", "Value": "+"},
            {"Token Type": "integer number", "Value": "12"},
            {"Token Type": "paren", "Value": ")"},
            {"Token Type": "operator", "Value": "/"},
            {"Token Type": "integer number", "Value": "14"},
        ],
    ]

    for tokens in tokens_list:
        print(f"Tokens: {tokens}")
        parser = Parser(tokens)
        tree = parser.parse()
        for pre, fill, node in RenderTree(tree):
            print(f"{pre}{node.name}")


if __name__ == "__main__":
    main()
