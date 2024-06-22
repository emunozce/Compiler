from typing import List, Union

class ASTNode:
    def __init__(self, node_type, value=None):
        self.node_type = node_type
        self.value = value
        self.children = []

    def add_child(self, child_node):
        self.children.append(child_node)

    def __repr__(self):
        return f"{self.node_type}({self.value}, {self.children})"

class Parser:
    def __init__(self, tokens: List[dict]):
        self.tokens = tokens
        self.current_token = 0
        self.ast = None

    def parse(self):
        self.ast = self.programa()
        return self.ast

    def consume(self):
        self.current_token += 1

    def lookahead(self) -> dict:
        if self.current_token < len(self.tokens):
            return self.tokens[self.current_token]
        return None

    def match(self, token_type: str) -> Union[str, None]:
        token = self.lookahead()
        if token and token_type in token:
            value = token[token_type]
            self.consume()
            return value
        raise SyntaxError(f"Expected {token_type}, found {token}")

    def programa(self):
        node = ASTNode("programa")
        if self.match("Reserved Word") == "main":
            self.match("Symbol")  # {
            node.add_child(self.lista_declaracion())
            self.match("Symbol")  # }
        else:
            raise SyntaxError("Expected 'main'")
        return node

    def lista_declaracion(self):
        node = ASTNode("lista_declaracion")
        while self.lookahead() and (self.lookahead().get("Reserved Word") in ["int", "double"] or self.lookahead().get("Identifier")):
            node.add_child(self.declaracion())
        return node

    def declaracion(self):
        if self.lookahead().get("Reserved Word") in ["int", "double"]:
            return self.declaracionVariable()
        else:
            return self.listaSentencias()

    def declaracionVariable(self):
        node = ASTNode("declaracionVariable")
        node.add_child(ASTNode("tipo", self.match("Reserved Word")))
        node.add_child(self.identificador())
        self.match("Symbol")  # ;
        return node

    def identificador(self):
        node = ASTNode("identificador")
        node.add_child(ASTNode("id", self.match("Identifier")))
        while self.lookahead() and self.lookahead().get("Symbol") == ",":
            self.match("Symbol")  # ,
            node.add_child(ASTNode("id", self.match("Identifier")))
        return node

    def listaSentencias(self):
        node = ASTNode("listaSentencias")
        while self.lookahead() and (self.lookahead().get("Reserved Word") in ["if", "while", "do", "cin", "cout"] or self.lookahead().get("Identifier")):
            node.add_child(self.sentencia())
        return node

    def sentencia(self):
        token = self.lookahead()
        if token.get("Reserved Word") == "if":
            return self.seleccion()
        elif token.get("Reserved Word") == "while":
            return self.iteracion()
        elif token.get("Reserved Word") == "do":
            return self.repeticion()
        elif token.get("Reserved Word") == "cin":
            return self.sentIn()
        elif token.get("Reserved Word") == "cout":
            return self.sentOut()
        elif token.get("Identifier"):
            return self.asignacion()
        else:
            raise SyntaxError(f"Unexpected token: {token}")

    def seleccion(self):
        node = ASTNode("seleccion")
        self.match("Reserved Word")  # if
        node.add_child(self.expresion())
        self.match("Reserved Word")  # then
        node.add_child(self.sentencia())
        if self.lookahead() and self.lookahead().get("Reserved Word") == "else":
            self.match("Reserved Word")  # else
            node.add_child(self.sentencia())
        self.match("Reserved Word")  # end
        return node

    def iteracion(self):
        node = ASTNode("iteracion")
        self.match("Reserved Word")  # while
        node.add_child(self.expresion())
        self.match("Reserved Word")  # do
        node.add_child(self.sentencia())
        self.match("Reserved Word")  # end
        return node

    def repeticion(self):
        node = ASTNode("repeticion")
        self.match("Reserved Word")  # do
        node.add_child(self.sentencia())
        self.match("Reserved Word")  # while
        node.add_child(self.expresion())
        self.match("Reserved Word")  # end
        return node

    def sentIn(self):
        node = ASTNode("sentIn")
        self.match("Reserved Word")  # cin
        node.add_child(ASTNode("id", self.match("Identifier")))
        self.match("Symbol")  # ;
        return node

    def sentOut(self):
        node = ASTNode("sentOut")
        self.match("Reserved Word")  # cout
        node.add_child(self.expresion())
        self.match("Symbol")  # ;
        return node

    def asignacion(self):
        node = ASTNode("asignacion")
        node.add_child(ASTNode("id", self.match("Identifier")))
        self.match("Assignment")  # =
        node.add_child(self.sentExpresion())
        return node

    def sentExpresion(self):
        node = ASTNode("sentExpresion")
        if self.lookahead() and self.lookahead().get("Symbol") == ";":
            self.match("Symbol")  # ;
        else:
            node.add_child(self.expresion())
            self.match("Symbol")  # ;
        return node

    def expresion(self):
        node = ASTNode("expresion")
        node.add_child(self.expresionSimple())
        if self.lookahead() and self.lookahead().get("Relational Operator"):
            node.add_child(ASTNode("relOp", self.match("Relational Operator")))
            node.add_child(self.expresionSimple())
        return node

    def expresionSimple(self):
        node = ASTNode("expresionSimple")
        node.add_child(self.termino())
        while self.lookahead() and self.lookahead().get("Arithmetic Operator") in ["+", "-"]:
            node.add_child(ASTNode("arithOp", self.match("Arithmetic Operator")))
            node.add_child(self.termino())
        return node

    def termino(self):
        node = ASTNode("termino")
        node.add_child(self.factor())
        while self.lookahead() and self.lookahead().get("Arithmetic Operator") in ["*", "/", "%"]:
            node.add_child(ASTNode("arithOp", self.match("Arithmetic Operator")))
            node.add_child(self.factor())
        return node

    def factor(self):
        node = ASTNode("factor")
        node.add_child(self.componente())
        while self.lookahead() and self.lookahead().get("Arithmetic Operator") in ["^"]:
            node.add_child(ASTNode("arithOp", self.match("Arithmetic Operator")))
            node.add_child(self.componente())
        return node

    def componente(self):
        token = self.lookahead()
        if token.get("Symbol") == "(":
            self.match("Symbol")  # (
            node = self.expresion()
            self.match("Symbol")  # )
        elif token.get("Integer Number"):
            node = ASTNode("int", self.match("Integer Number"))
        elif token.get("Real Number"):
            node = ASTNode("real", self.match("Real Number"))
        elif token.get("Identifier"):
            node = ASTNode("id", self.match("Identifier"))
        else:
            raise SyntaxError(f"Unexpected token: {token}")
        return node
