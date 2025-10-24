import sys
from parser import parse
from ast_nodes import *

def print_ast(node, indent=0):
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

if __name__ == "__main__":
    # Lee entrada desde archivo o stdin
    if len(sys.argv) > 1:
        with open(sys.argv[1], "r") as f:
            source = f.read()
    else:
        source = sys.stdin.read()

    print("🔹 Resultado del análisis sintáctico (AST):\n")
    try:
        program_ast = parse(source)
        print_ast(program_ast)
    except Exception as e:
        print(f"❌ Error: {e}")
