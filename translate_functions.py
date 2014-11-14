"""
(c) Daniel Hones 2014

MIT License


This file contains definitions for functions that perform necessary operations to
PrettyEquation objects.
"""

from constants import *

def insert_frac(equation):
    """
    Insert \frac and accoutrement in the right places when user presses slash
    """

    # Really need to think this one through.
    if equation.previous_keypress == '' or equation.previous_keypress.char in SPECIAL_CHARS:
        return

def insert_parens(equation):
    return

