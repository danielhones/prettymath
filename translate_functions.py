"""
(c) Daniel Hones 2014

MIT License


This file contains definitions for functions that perform necessary operations to
PrettyEq objects.
"""

from constants import *


def get_current_list(index, nested_list):
    """
    Gets passed index, which is a list, and nested_list and determines which (if any) list inside the nested latex
    eq list is the one currently being edited.  Returns the current list
    """
    if len(index) == 1:
        return nested_list
    else:
        result = []
        # Leave off the last element in index because that points to the element itself, not the
        # list containing it, which is what we want:
        for i in index[:-1]:
            result.append(i)
        # First turn the integer elements of result into strings, then join them with '][' so
        # they're in the format of a list index, then put the outer brackets on
        return eval('nested_list' + '[' + ']['.join(map(str, result)) + ']')

def move_cursor(eq, direction):
    """
    TODO:
    Need to modify this so that it can navigate to the end of the equation and append a new character,
    and go INSIDE nested lists, not just exit from them.  Might require a little different approach
    """
    if direction == LEFT:
        motion = -1
    elif direction == RIGHT:
        motion = 1

    last_index = eq.latex_index[-1]
    next_index = last_index + motion
    
    # Check if trying to move beyond bounds of whole equation:
    out_of_bounds = (len(eq.latex_index) == 1) and (next_index < 0 or next_index == len(eq.latex))
    if out_of_bounds:
        return

    current_list = get_current_list(eq.latex_index, eq.latex)        
    next_element = current_list[next_index]

    # Check if moving to edge (ie. into first or last position) of an inner list.
    # Since these will contain LaTeX commands, move out of the list to preserve the list structure
    moving_to_edge = (len(eq.latex_index) > 1) and (next_index = 0 or next_index == len(eq.latex) - 1) 
    if moving_to_edge:
        del current_list[last_index]
        eq.latex_index.pop()
        eq.latex.insert(eq.latex_index[-1], CURSOR)


    # Fall through case, swap cursor with the appropriate adjacent element:
    current_list[last_index], current_list[next_index] = current_list[next_index], current_list[last_index]

    return

def cursor_up(eq, keycode):
    return
    
def cursor_down(eq, keycode):
    return
    
def insert_frac(eq):
    """
    Insert \frac and accoutrement in the right places when user presses slash
    """
    current_list = get_current_list(eq.latex_index, eq.latex)
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
    current_list = get_current_list(eq.latex_index, eq.latex)
    # Delete cursor symbol
    del current_list[eq.latex_index[-1]]
    # insert the list containing the subscript. Use arrow keys to navigate out of it:
    current_list.insert(eq.latex_index[-1], ['_{', '|', '}'])
    # Add new level to latex_index:
    eq.latex_index.append(1)
    return

def insert_superscript(eq):
    current_list = get_current_list(eq.latex_index, eq.latex)
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
    current_list = get_current_list(eq.latex_index, eq.latex)    
    # Delete cursor symbol
    del current_list[eq.latex_index[-1]]
    # insert the list containing the subscript. Use arrow keys to navigate out of it:
    # '\right.' places an invisible right element so that there will just be a left parenthese
    # until the user types the right one.
    current_list.insert(eq.latex_index[-1], [r'\left(', '|', r'\right.'])
    # Add new level to latex_index:
    eq.latex_index.append(1)

    return

def close_parens(eq):
    """
    called when ')' is typed explicitly or when the ) is navigated past using arrow keys.
    Need to figure out how to handle an attempt to delete just one of the parentheses
    """
    current_list = get_current_list(eq.latex_index, eq.latex)
    current_list[-1] = r'\right)'
    return