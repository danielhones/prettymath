import ply.lex as lex


tokens = (
    'INTEGER',
    'FLOAT',
    'VARIABLE',
    'COMMAND',
    'ARGUMENT',
    'EXPONENT',
    'SUBSCRIPT',
    'TIMES',
    'PLUS',
    'MINUS',
    'ASSIGN',  # This is the equal sign
    'EQUALS',  # This is equivalence in Python.  Not sure if we need this.
)
t_VARIABLE = r'[a-zA-Z]{1}'
t_FLOAT = r'\d+\.\d+|\.\d+'
t_INTEGER = r'\d+'
t_EXPONENT = r'\^'
t_PLUS = r'\+'
t_MINUS = r'\-'
t_SUBSCRIPT = r'\_'
t_ASSIGN = '='
t_EQUALS = '=='
t_ignore = ' \t\n'
states = (
    ('inarg', 'exclusive'),  # Not sure if exclusive is right here
)


# These two may not need to be defined as functions:
def t_TIMES(t):
    r'\\cdot|\*'
    return t

def t_COMMAND(t):
    r'\\[a-zA-Z]+'
    return t

def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)


# Adapted from PLY documentation, section 4.19:
def t_inarg(t):
    r'\{'
    t.lexer.arg_start = t.lexer.lexpos
    t.lexer.brace_level = 1
    t.lexer.begin('inarg')

def t_inarg_lbrace(t):
    r'\{'
    t.lexer.brace_level += 1

def t_inarg_rbrace(t):
    r'\}'
    t.lexer.brace_level -= 1

    # If closing brace, return the argument
    if t.lexer.brace_level == 0:
        # t.value might have an off by one:
        t.value = t.lexer.lexdata[t.lexer.arg_start:t.lexer.lexpos-1]
        t.type = "ARGUMENT"
        t.lexer.begin('INITIAL')
        return t

t_inarg_ignore = ' \t\n'

def t_inarg_error(t):
    t.lexer.skip(1)
