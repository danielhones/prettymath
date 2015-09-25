"""
Maybe a rule-based approach is good here?
For example:

\frac{num}{denom} -> ((num)/(denom))
x_{string}        -> x_string
3abc              -> 3*a*b*c
x^{expr}          -> x**(expr)

I wonder if this is feasible to implement this way.
"""

from collections import deque
import latex_lexer
from ply import lex


def pass_through(x):
    return x


# Maybe make this a class called TokenTranslator or something, where the actions to take are defined
# as methods, with an additional method that looks up the appropriate action in a table and applies it.
TRANSLATE_TABLE = {
    'VARIABLE': pass_through,
    'FLOAT': pass_through,
    'INTEGER': lambda x: x + '.0',
}


def latex_to_python(latex):
    """
    Given a LaTeX math string, return a corresponding Python expression
    """
    lexer = lex.lex(module=latex_lexer)
    lexer.input(latex)
    result = []

    while True:
        token = lexer.token()
        if not token:
            break

        if token.type == 'VARIABLE':
            result.append(token.value)
        elif token.type == 'INTEGER':
            result.append(token.value + '.0')
        elif token.type == 'FLOAT':
            result.append(token.value)
        elif token.type == 'PLUS':
            result.append(token.value)
        elif token.type == 'MINUS':
            result.append(token.value)
        elif token.type == 'TIMES':
            result.append('*')
        elif token.type == 'COMMAND':
            if token.value == '\\frac':
                arg1 = lexer.token()
                arg2 = lexer.token()
                result.append('(')
                result.append(parenthesize(latex_to_python(arg1.value)))
                result.append('/')
                result.append(parenthesize(latex_to_python(arg2.value)))
                result.append(')')
        elif token.type == 'EXPONENT':
            result.append('**')
            arg = lexer.token()  # break this into function get_next_arg
            result.append(parenthesize(latex_to_python(arg.value)))
        elif token.type == 'ARGUMENT':
            arg = latex_to_python(token.value)
            result.append(arg)  # This might be right, I dunno

    return ''.join(result)


def parenthesize(x):
    """Return a copy of x surrounded by open and close parentheses"""
    cast = type(x)
    if cast is deque:
        return deque(['('] + list(x) + [')'])
    return cast('(') + x + cast(')')


class LatexTranslationError(Exception):
    pass
