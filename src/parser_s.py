from pathlib import Path
import ply.yacc as yacc
from lexer import get_lexical_analysis, Token


# Token list required by PLY
tokens = [
    "IDENTIFIER",
    "INTEGER_NUMBER",
    "REAL_NUMBER",
    "INCREMENT_OPERATOR",
    "DECREMENT_OPERATOR",
    "SYMBOL",
    "ASSIGNMENT",
    "EQ",
    "RELATIONAL_OPERATOR",
    "LOGICAL_OPERATOR",
    "ARITHMETIC_OPERATOR",
    "RESERVED_WORD",
]


# Grammar rules
def p_programa(p):
    """programa : RESERVED_WORD LPAREN RPAREN LBRACE listaDeclaracion RBRACE"""
    p[0] = ("program", p[5])


def p_listaDeclaracion(p):
    """listaDeclaracion : listaDeclaracion declaracion
    | declaracion"""
    if len(p) == 3:
        p[0] = p[1] + [p[2]]
    else:
        p[0] = [p[1]]


def p_declaracion(p):
    """declaracion : declaracionVariable
    | listaSentencias"""
    p[0] = p[1]


def p_declaracionVariable(p):
    """declaracionVariable : tipo identificador SEMICOLON"""
    p[0] = ("declaration", p[1], p[2])


def p_identificador(p):
    """identificador : identificador COMMA IDENTIFIER
    | IDENTIFIER"""
    if len(p) == 4:
        p[0] = p[1] + [p[3]]
    else:
        p[0] = [p[1]]


def p_tipo(p):
    """tipo : RESERVED_WORD"""
    p[0] = p[1]


def p_listaSentencias(p):
    """listaSentencias : listaSentencias sentencia
    | empty"""
    if len(p) == 3:
        p[0] = p[1] + [p[2]]
    else:
        p[0] = []


def p_sentencia(p):
    """sentencia : seleccion
    | iteracion
    | repeticion
    | sentIn
    | sentOut
    | asignacion"""
    p[0] = p[1]


def p_asignacion(p):
    """asignacion : IDENTIFIER ASSIGNMENT sentExpresion"""
    p[0] = ("assign", p[1], p[3])


def p_sentExpresion(p):
    """sentExpresion : expresion SEMICOLON
    | SEMICOLON"""
    if len(p) == 3:
        p[0] = p[1]
    else:
        p[0] = None


def p_seleccion(p):
    """seleccion : RESERVED_WORD expresion sentencia RESERVED_WORD
    | RESERVED_WORD expresion sentencia RESERVED_WORD sentencia RESERVED_WORD"""
    if len(p) == 5:
        p[0] = ("if", p[2], p[3])
    else:
        p[0] = ("if-else", p[2], p[3], p[5])


def p_iteracion(p):
    """iteracion : RESERVED_WORD expresion sentencia RESERVED_WORD"""
    p[0] = ("while", p[2], p[3])


def p_repeticion(p):
    """repeticion : RESERVED_WORD sentencia RESERVED_WORD expresion"""
    p[0] = ("do-while", p[2], p[4])


def p_sentIn(p):
    """sentIn : RESERVED_WORD IDENTIFIER SEMICOLON"""
    p[0] = ("cin", p[2])


def p_sentOut(p):
    """sentOut : RESERVED_WORD expresion SEMICOLON"""
    p[0] = ("cout", p[2])


def p_expresion(p):
    """expresion : expresionSimple RELATIONAL_OPERATOR expresionSimple
    | expresionSimple"""
    if len(p) == 4:
        p[0] = ("relation", p[1], p[2], p[3])
    else:
        p[0] = p[1]


def p_expresionSimple(p):
    """expresionSimple : expresionSimple LOGICAL_OPERATOR termino
    | termino"""
    if len(p) == 4:
        p[0] = ("logic", p[1], p[2], p[3])
    else:
        p[0] = p[1]


def p_termino(p):
    """termino : termino ARITHMETIC_OPERATOR factor
    | factor"""
    if len(p) == 4:
        p[0] = ("arith", p[1], p[2], p[3])
    else:
        p[0] = p[1]


def p_factor(p):
    """factor : factor ARITHMETIC_OPERATOR componente
    | componente"""
    if len(p) == 4:
        p[0] = ("arith", p[1], p[2], p[3])
    else:
        p[0] = p[1]


def p_componente(p):
    """componente : LPAREN expresion RPAREN
    | INTEGER_NUMBER
    | REAL_NUMBER
    | IDENTIFIER"""
    if len(p) == 4:
        p[0] = p[2]
    else:
        p[0] = p[1]


def p_empty(p):
    """empty :"""
    p[0] = None


def p_error(p):
    print(f"Syntax error at '{p.value}'")


# Build the parser
parser = yacc.yacc()


def parse_file(file: Path):
    tokens, errors = get_lexical_analysis(file)
    if errors:
        print("Errors found during lexical analysis:")
        for error in errors:
            print(error)
    else:
        result = parser.parse(lexer=iter(tokens))
        print(result)


if __name__ == "__main__":
    file_path = Path("test_sintactico.txt")
    if file_path.exists():
        parse_file(file_path)
    else:
        print("File does not exist")
