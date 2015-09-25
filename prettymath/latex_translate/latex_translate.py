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


def latex_to_python(latex):
    """
    Given a LaTeX math string, return a corresponding Python expression
    """
    # How to approach this?
    # Maybe parse it from left to right, or maybe come up with an appropriate order of operations
    # such as: replace numbers, replace variables, replace latex commands, handle operators
    # like ^ and _, etc
    # Do some research and thinking on it.
    # Also, is it best to deal with latex as a string using indexes to refer to substrings, or split it
    # into a list of characters, or something else?
    pass


def parenthesize(x):
    """Return x surrounded by open and close parentheses"""
    cast = type(x)
    if cast is deque:
        x.appendleft('(')
        x.append(')')
        return x
    return cast('(') + x + cast(')')


class LatexTranslationError(Exception):
    pass
