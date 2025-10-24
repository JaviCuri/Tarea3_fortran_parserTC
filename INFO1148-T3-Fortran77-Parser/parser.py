from lexer import Lexer
from ast_nodes import *

# ==========================================================
#  Parser LL(1) recursivo descendente para un subconjunto de FORTRAN77
# ==========================================================

class ParseError(Exception):
    """Error sintáctico"""
    pass


class Parser:
    def __init__(self, text, trace=False):
        self.tokens = list(Lexer(text).tokens())
        self.i = 0
        self.trace = trace

    # ------------------- utilidades -------------------

    def cur(self):
        """Token actual"""
        return self.tokens[self.i]

    def eat(self, t):
        """Consume un token si coincide, si no lanza error"""
        if self.cur().type == t:
            if self.trace:
                print(f"EAT {self.cur()}")
            self.i += 1
        else:
            c = self.cur()
            raise ParseError(f"Se esperaba {t} y llegó {c.type} ({c.value!r}) en línea {c.line}:{c.col}")

    # ------------------- reglas principales -------------------

    def parse_program(self):
        # program -> PROGRAM IDENT NEWLINE stmt_list END NEWLINE? EOF
        self.eat("PROGRAM")
        name_tok = self.cur()
        self.eat("IDENT")
        self.eat("NEWLINE")
        stmts = self.parse_stmt_list()
        self.eat("END")
        if self.cur().type == "NEWLINE":
            self.eat("NEWLINE")
        self.eat("EOF")
        return Program(name_tok.value, stmts)

    def parse_stmt_list(self):
        # stmt_list -> { stmt NEWLINE }*
        stmts = []
        while self.cur().type not in ("END", "EOF"):
            if self.cur().type == "NEWLINE":
                self.eat("NEWLINE")
                continue
            stmt = self.parse_stmt()
            stmts.append(stmt)
            if self.cur().type == "NEWLINE":
                self.eat("NEWLINE")
        return stmts

    def parse_stmt(self):
        # stmt -> decl | assign | do_stmt
        t = self.cur().type
        if t in ("INTEGER", "REAL"):
            return self.parse_decl()
        elif t == "DO":
            return self.parse_do()
        else:
            return self.parse_assign()

    # ------------------- declaraciones -------------------

    def parse_decl(self):
        # decl -> (INTEGER|REAL) idlist
        kind = self.cur().type
        self.eat(kind)
        ids = self.parse_idlist()
        return Decl(kind, ids)

    def parse_idlist(self):
        # idlist -> IDENT { ',' IDENT }*
        ids = []
        tok = self.cur()
        self.eat("IDENT")
        ids.append(tok.value)
        while self.cur().type == "COMMA":
            self.eat("COMMA")
            tok = self.cur()
            self.eat("IDENT")
            ids.append(tok.value)
        return ids

    # ------------------- asignaciones y DO -------------------

    def parse_assign(self):
        # assign -> IDENT '=' expr
        name = self.cur().value
        self.eat("IDENT")
        self.eat("EQ")
        e = self.parse_expr()
        return Assign(name, e)

    def parse_do(self):
        # do_stmt -> DO IDENT '=' expr ',' expr
        self.eat("DO")
        var = self.cur().value
        self.eat("IDENT")
        self.eat("EQ")
        start = self.parse_expr()
        self.eat("COMMA")
        end = self.parse_expr()
        return DoStmt(var, start, end)

    # ------------------- expresiones -------------------

    def parse_expr(self):
        # expr -> term { ('+'|'-') term }*
        node = self.parse_term()
        while self.cur().type in ("PLUS", "MINUS"):
            op = self.cur().type
            self.eat(op)
            right = self.parse_term()
            node = BinOp(op, node, right)
        return node

    def parse_term(self):
        # term -> factor { ('*'|'/') factor }*
        node = self.parse_factor()
        while self.cur().type in ("STAR", "SLASH"):
            op = self.cur().type
            self.eat(op)
            right = self.parse_factor()
            node = BinOp(op, node, right)
        return node

    def parse_factor(self):
        # factor -> NUMBER | IDENT | '(' expr ')' | power
        tok = self.cur()
        if tok.type == "LPAREN":
            self.eat("LPAREN")
            e = self.parse_expr()
            self.eat("RPAREN")
            if self.cur().type == "POWER":
                self.eat("POWER")
                right = self.parse_factor()
                return Power(e, right)
            return e
        elif tok.type == "NUMBER":
            self.eat("NUMBER")
            node = Number(tok.value)
            if self.cur().type == "POWER":
                self.eat("POWER")
                right = self.parse_factor()
                return Power(node, right)
            return node
        elif tok.type == "IDENT":
            self.eat("IDENT")
            node = Ident(tok.value)
            if self.cur().type == "POWER":
                self.eat("POWER")
                right = self.parse_factor()
                return Power(node, right)
            return node
        else:
            raise ParseError(f"factor inválido en línea {tok.line}:{tok.col} ({tok.value})")


def parse(text, trace=False):
    """Función de conveniencia"""
    return Parser(text, trace).parse_program()


# ==========================================================
# Bloque de prueba local
# ==========================================================
if __name__ == "__main__":
    sample = """\
PROGRAM DEMO
INTEGER A, B
A = 2
B = A**2 + 1
DO A = 1, 3
END
"""
    print("🔹 Análisis sintáctico:\n")
    ast = parse(sample)
    print(ast)
