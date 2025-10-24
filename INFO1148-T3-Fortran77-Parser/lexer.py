import re

# Palabras clave
KEYWORDS = {"PROGRAM", "END", "INTEGER", "REAL", "DO"}

# Definición de tokens
TOKEN_SPEC = [
    ("SKIP_WS",   r"[ \t]+"),
    ("COMMENT",   r"^[cC].*$"),   # Comentario: línea que empieza con C/c
    ("NEWLINE",   r"\r?\n"),
    ("POWER",     r"\*\*"),
    ("PLUS",      r"\+"),
    ("MINUS",     r"-"),
    ("STAR",      r"\*"),
    ("SLASH",     r"/"),
    ("EQ",        r"="),
    ("COMMA",     r","),
    ("LPAREN",    r"\("),
    ("RPAREN",    r"\)"),
    ("NUMBER",    r"\d+(\.\d+)?"),
    ("IDENT",     r"[A-Za-z][A-Za-z0-9_]*"),
]

# Compilamos la expresión regular maestra con flag MULTILINE
MASTER_RE = re.compile(
    "|".join(f"(?P<{name}>{pat})" for name, pat in TOKEN_SPEC),
    re.MULTILINE,
)

class Token:
    __slots__ = ("type", "value", "line", "col")
    def __init__(self, t, v, line, col):
        self.type, self.value, self.line, self.col = t, v, line, col
    def __repr__(self):
        return f"Token({self.type!s},{self.value!r}@{self.line}:{self.col})"

class Lexer:
    def __init__(self, text):
        self.text = text

    def _emit(self, t, v, line, col):
        if t == "IDENT":
            up = v.upper()
            if up in KEYWORDS:
                return Token(up, up, line, col)
        return Token(t, v, line, col)

    def tokens(self):
        pos = 0
        line = 1
        col = 1
        text = self.text

        while pos < len(text):
            m = MASTER_RE.match(text, pos)
            if not m:
                raise SyntaxError(f"Carácter inesperado {text[pos]!r} en {line}:{col}")
            kind = m.lastgroup
            val = m.group(kind)
            start_line = line
            start_col = col
            pos = m.end()

            if kind == "NEWLINE":
                yield Token("NEWLINE", "\n", start_line, start_col)
                line += 1
                col = 1
                continue
            elif kind == "SKIP_WS" or kind == "COMMENT":
                # comentarios o espacios: solo saltar
                if kind == "COMMENT":
                    yield Token("NEWLINE", "\n", start_line, start_col)
                span = m.end() - m.start()
                col += span
                continue
            else:
                tok = self._emit(kind, val, start_line, start_col)
                yield tok
                col += len(val)

        yield Token("EOF", "", line, col)

# ==========================================================
# Bloque de prueba
# ==========================================================
if __name__ == "__main__":
    text = """\
PROGRAM DEMO
C esto es un comentario
INTEGER A, B
A = 3
B = A**2 + 1
END
"""
    print("🔹 Tokens generados:\n")
    for tok in Lexer(text).tokens():
        print(tok)
