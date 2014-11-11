"""
(c) Daniel Hones 2014

MIT License


This file contains definitions for functions that perform necessary operations to
PrettyEquation objects.
"""

from mathentry_constants import *

def insert_frac(equation):
    """
    Insert \frac and accoutrement in the right places when user presses slash
    """

    # Really need to think this one through.
    if equation.previous_keypress == '' or equation.previous_keypress.char in SPECIAL_CHARS:
        equation.active_term = [r'\frac', '{', '|', '}{', '}']
        equation.tex_index.append(2)
#        equation.active_term.insert(2, '{')
#        equation.active_term.insert( equation.tex_index[-1] + 1, '}{' )
#        equation.active_term.append('}')
        return

def insert_parens(equation):
    return
