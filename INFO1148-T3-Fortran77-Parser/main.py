from parser import parse
from ast_nodes import *

# ==========================================================
# Programa principal - muestra el árbol sintáctico (AST)
# ==========================================================

def print_ast(node, indent=0):
    """Imprime el árbol sintáctico de forma legible."""
    pad = "  " * indent

    if isinstance(node, Program):
        print(f"{pad}Program {node.name}")
        for s in node.statements:
            print_ast(s, indent + 1)

    elif isinstance(node, Decl):
        print(f"{pad}Decl {node.kind}: {', '.join(node.idlist)}")

    elif isinstance(node, Assign):
        print(f"{pad}Assign {node.ident} =")
        print_ast(node.expr, indent + 1)

    elif isinstance(node, DoStmt):
        print(f"{pad}Do {node.loopvar} =")
        print_ast(node.start, indent + 1)
        print_ast(node.end, indent + 1)

    elif isinstance(node, BinOp):
        op_symbol = {'PLUS': '+', 'MINUS': '-', 'STAR': '*', 'SLASH': '/'}[node.op]
        print(f"{pad}BinOp {op_symbol}")
        print_ast(node.left, indent + 1)
        print_ast(node.right, indent + 1)

    elif isinstance(node, Power):
        print(f"{pad}Power **")
        print_ast(node.left, indent + 1)
        print_ast(node.right, indent + 1)

    elif isinstance(node, Number):
        print(f"{pad}Number {node.value}")

    elif isinstance(node, Ident):
        print(f"{pad}Ident {node.name}")

    else:
        print(f"{pad}{node}")


if __name__ == "__main__":
    source = """\
PROGRAM demo
C ejemplo de FORTRAN reducido
INTEGER i, j
REAL x
i = 1
x = (i + 3.5) * 2
DO j = 1, 10
END
"""

    print("🔹 Resultado del análisis sintáctico (AST):\n")
    program_ast = parse(source)
    print_ast(program_ast)

