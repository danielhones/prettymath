"""
TODO: consider making a LatexTranslater class, since all the functions and nested functions
perform operations on the same object (lexer).  lexer could be an attribute of the class,
rather than passing it through the function calls.  Works either way, which is cleaner?
"""

from collections import deque
import latex_lexer
from ply import lex


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
        result.append(translate_token(token, lexer))
    return ''.join(result)


def translate_token(token, lexer):
    def get_next_arg():
        return lexer.token()

    def pass_through():
        return token.value

    def VARIABLE():
        if token.value == 'e':
            return 'math.e'
        else:
            return pass_through()

    def INTEGER():
        return token.value + '.0'

    def COMMAND():
        return translate_command(token, lexer)

    def TIMES():
        return '*'

    def EXPONENT():
        result = ['**']
        arg = get_next_arg()
        # I think this works here:
        result.append(parenthesize(latex_to_python(arg.value)))
        return ''.join(result)

    def ARGUMENT():
        translated_arg = latex_to_python(token.value)
        return translated_arg

    try:
        return eval(token.type)()
    except NameError:
        # Default behavior is pass_through():
        return pass_through()


def translate_command(token, lexer):
    def get_next_arg():
        return lexer.token()

    def frac():
        arg1 = get_next_arg()
        arg2 = get_next_arg()
        result = ['(']
        result.append(parenthesize(latex_to_python(arg1.value)))
        result.append('/')
        result.append(parenthesize(latex_to_python(arg2.value)))
        result.append(')')
        return ''.join(result)

    def pi():
        return 'math.pi'

    def sin():
        # TODO: write a function get_next_term() or something that returns the part that should
        # go inside the parens for math.sin, if there are not existing parens.  **Or always include
        # explicit parens from the PrettyExpression class.
        return 'math.sin'

    def cos():
        return 'math.cos'

    command_name = token.value[1:].strip()
    try:
        return eval(command_name)()
    except NameError:
        raise LatexTranslationError("Couldn't translate token " + token.type + ' with value ' + token.value)


def parenthesize(x):
    """Return a copy of x surrounded by open and close parentheses"""
    cast = type(x)
    if cast is deque:
        return deque(['('] + list(x) + [')'])
    return cast('(') + x + cast(')')


class LatexTranslationError(Exception):
    pass
