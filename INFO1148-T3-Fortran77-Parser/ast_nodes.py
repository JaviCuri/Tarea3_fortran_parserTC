from dataclasses import dataclass
from typing import List, Union

# ==========================================================
# Definición de los nodos del Árbol Sintáctico Abstracto (AST)
# ==========================================================

@dataclass
class Program:
    name: str
    statements: list

@dataclass
class Decl:
    kind: str        # "INTEGER" | "REAL"
    idlist: list     # [str]

@dataclass
class Assign:
    ident: str
    expr: "Expr"

@dataclass
class DoStmt:
    loopvar: str
    start: "Expr"
    end: "Expr"

# ---------------------- Expresiones ----------------------

@dataclass
class BinOp:
    op: str
    left: "Expr"
    right: "Expr"

@dataclass
class Power:
    left: "Expr"
    right: "Expr"

@dataclass
class Number:
    value: str

@dataclass
class Ident:
    name: str

# Tipos generales para referencia en el parser
Expr = Union[BinOp, Power, Number, Ident]
Stmt = Union[Decl, Assign, DoStmt]


