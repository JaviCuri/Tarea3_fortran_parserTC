import re

KEYWORDS = {"PROGRAM", "END", "INTEGER", "REAL", "DO"}

TOKEN_SPEC = [
    ("SKIP_WS",   r"[ \t]+"),
    ("COMMENT",   r"(?m)^([cC].*)$"),              # línea que inicia con C/c
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

MASTER_RE = re.compile("|".join(f"(?P<{name}>{pat})" for name, pat in TOKEN_SPEC))

class Token:
    __slots__ = ("type","value","line","col")
    def __init__(self, t, v, line, col): self.type, self.value, self.line, self.col = t, v, line, col
    def __repr__(self): return f"Token({self.type},{self.value!r}@{self.line}:{self.col})"

class Lexer:
    def __init__(self, text):
        self.text = text
        self.pos = 0
        self.line = 1
        self.col  = 1
        self.len  = len(text)

    def _emit(self, t, v, start_line, start_col):
        if t == "IDENT":
            up = v.upper()
            if up in KEYWORDS:
                return Token(up, up, start_line, start_col)
        return Token(t, v, start_line, start_col)

    def tokens(self):
        pos = 0
        line = 1
        col  = 1
        text = self.text
        while pos < len(text):
            m = MASTER_RE.match(text, pos)
            if not m:
                raise SyntaxError(f"Carácter inesperado {text[pos]!r} en {line}:{col}")
            kind = m.lastgroup
            val  = m.group(kind)
            start_col = col
            start_line= line
            pos = m.end()

            if kind == "NEWLINE":
                yield Token("NEWLINE", "\n", start_line, start_col)
                line += 1
                col = 1
                continue
            elif kind == "SKIP_WS" or kind == "COMMENT":
                # comentario ignora hasta fin de línea (COMMENT ya consumió la línea)
                if kind == "COMMENT":
                    # forzamos fin de línea si no lo hay
                    if pos < len(text) and text[pos-1] != "\n":
                        yield Token("NEWLINE", "\n", start_line, start_col)
                # ajustar columnas
                span = m.end() - m.start()
                col += span
                continue
            else:
                tok = self._emit(kind, val, start_line, start_col)
                yield tok
                col += len(val)
        yield Token("EOF", "", line, col)
