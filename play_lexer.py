from ply import lex
from prettymath import latex_lexer


lexer = lex.lex(module=latex_lexer)


def tokenize(x):
    lexer.input(x)
    for t in lexer:
        print t.type + ': ' + t.value

while True:
    tokenize(raw_input('> '))
