"""
(c) Daniel Hones 2014

MIT License


This file contains definitions for functions that perform necessary operations to
PrettyEq objects.
"""

from constants import *

def get_full_index(index):
    # May not need this function
    return

def get_current_list_index(index):
    """
    Gets passed index, which is a list, and determines which (if any) list inside the nested latex
    eq list is the one currently being edited.  Returns a string in the format [a][b][c] so it 
    can be used with eval() in other functions to get the current list.
    """
    if len(index) == 1:
        return ''
    else:
        result = []
        # Leave off the last element in index because that points to the element itself, not the
        # list containing it, which is what we want.
        for i in index[:-1]:
            result.append(i)
        # First turn the integer elements of result into strings, then join them with '][' so
        # they're in the format of a list index, then put the outer brackets on
        return '['+']['.join(map(str, result))+']'

def insert_frac(eq):
    """
    Insert \frac and accoutrement in the right places when user presses slash
    """
    current_list = eval('eq.latex' + get_current_list_index(eq.latex_index))
    # Delete cursor symbol
    del current_list[eq.latex_index[-1]]
    last_element = current_list[eq.latex_index[-1]-1]

    # If it's a new term, or the last element was something like sin, draw the bar and start entering the numerator:
    if eq.previous_keypress == '' or eq.previous_keypress.char in SPECIAL_CHARS or last_element in FUNCTIONS:
        current_list.insert(eq.latex_index[-1], [r'\frac{', '|', '}{', '}'])
        eq.latex_index.append(1)
    else:
        new_list = [r'\frac{'] + eq.running_list + ['}{', '|', '}']
        size = len(eq.running_list)
        # Erase previous term so it can go in numerator
        del current_list[ eq.latex_index[-1] - size : eq.latex_index[-1] ]
        current_list.insert(eq.latex_index[-1], new_list)
        # Add new level to latex_index:
        eq.latex_index[-1] -= size
        eq.latex_index.append(2+len(eq.running_list))
    # And reset running_list:
    eq.running_list = []
    return

def insert_subscript(eq):
    # this might be code that gets duplicated in a lot of these functions, see if there's better way to do it.
    current_list = eval('eq.latex' + get_current_list_index(eq.latex_index))
    # Delete cursor symbol
    del current_list[eq.latex_index[-1]]
    # insert the list containing the subscript. Use arrow keys to navigate out of it:
    current_list.insert(eq.latex_index[-1], ['_{', '|', '}'])
    # Add new level to latex_index:
    eq.latex_index.append(1)
    return

def insert_superscript(eq):
    current_list = eval('eq.latex' + get_current_list_index(eq.latex_index))
    # Delete cursor symbol
    del current_list[eq.latex_index[-1]]
    # insert the list containing the superscript. Use arrow keys to navigate out of it:
    current_list.insert(eq.latex_index[-1], ['^{', '|', '}'])
    # Add new level to latex_index:
    eq.latex_index.append(1)
    return

def open_parens(eq):
    """
    insert set of parentheses
    """
    current_list = eval('eq.latex' + get_current_list_index(eq.latex_index))
    # Delete cursor symbol
    del current_list[eq.latex_index[-1]]
    # insert the list containing the subscript. Use arrow keys to navigate out of it:
    current_list.insert(eq.latex_index[-1], [r'\left(', '|', '\right)'])
    # Add new level to latex_index:
    eq.latex_index.append(1)

    return

def close_parens(eq):
    """
    called when ')' is typed explicitly or when the ) is navigated past using arrow keys.
    Need to figure out how to handle an attempt to delete just one of the parentheses
    """
    return
