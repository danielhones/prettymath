import ply.lex as lex


tokens = (
    'INTEGER',
    'FLOAT',
    'COMMAND',
    'ARGUMENT',
    'ONEARGCOMMAND',
    'TWOARGCOMMAND',
)
literals = '+-abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ{}'
t_FLOAT = r'\d+\.\d+|\.\d+'
t_INTEGER = r'\d+'
t_ignore = ' \t'
states = (
    ('inarg', 'inclusive'),  # Not sure if inclusive is right here
)





def t_COMMAND(t):
    r'\\[a-zA-Z]+'
    return t




lexer = lex.lex()
data = r'\frac{10ab}{3.5xy}'
lexer.input(data)


def tokenize(data=None):
    if data:
        lexer.input(data)
    print 'Tokenizing:\n', lexer.lexdata
    for tok in lexer:
        print tok.type + ':', tok.value

tokenize()
