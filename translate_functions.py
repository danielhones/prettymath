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
    Get this working right.  Go step by step through conditions.  There's a bug somewhere.  Try starting from the
    top again.
    """
    if direction == LEFT:
        motion = -1
    elif direction == RIGHT:
        motion = 1

    current_list = get_current_list(eq.latex_index, eq.latex)
    current_index = eq.latex_index[-1]
    next_index = current_index + motion
    eq.running_list = []

    at_left_edge = (motion == -1) and (len(eq.latex_index) == 1) and (current_index == 0)
    at_right_edge = (motion == 1) and (len(eq.latex_index) == 1) and (current_index == len(eq.latex) - 1)

    print at_left_edge,at_right_edge
    
    """    
    # Check to see if moving left or right goes beyond bounds of current list:
    beyond_list = (next_index > len(current_list)) or (next_index < 0)
    print 'beyond_list:\t', beyond_list

    # First check if we're at the edge of the whole equation:
    at_boundary = beyond_list and len(eq.latex_index) == 1
    print 'at_boundary:\t', at_boundary
    if at_boundary:
        return
    
    # Remove cursor:
    del current_list[eq.latex_index[-1]]

    next_element = current_list[next_index]
    
    if type(next_element) is list:
        print 'next_element is a list'
        add_index = [None, 0, len(next_element) - 1]
        eq.latex_index[-1] == next_index
        eq.latex_index.append(add_index[motion])
        current_list = get_current_list(eq.latex_index, eq.latex)
        current_list.insert(eq.latex_index[-1], CURSOR)
    elif beyond_list:
        eq.latex_index.pop()
        eq.latex_index[-1] += motion
        eq.latex.insert( eq.latex_index[-1], CURSOR )
    elif next_index == len(current_list):
        eq.latex_index[-1] = next_index
        current_list.append(CURSOR) 
    else:
        eq.latex_index[-1] = next_index
        current_list.insert( eq.latex_index[-1], CURSOR )
    """
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
        current_list.insert(eq.latex_index[-1], [r'\frac{', CURSOR, '}{', '}'])
        eq.latex_index.append(1)
    else:
        new_list = [r'\frac{'] + eq.running_list + ['}{', CURSOR, '}']
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
    current_list.insert(eq.latex_index[-1], ['_{', CURSOR, '}'])
    # Add new level to latex_index:
    eq.latex_index.append(1)
    return

def insert_superscript(eq):
    current_list = get_current_list(eq.latex_index, eq.latex)
    # Delete cursor symbol
    del current_list[eq.latex_index[-1]]
    # insert the list containing the superscript. Use arrow keys to navigate out of it:
    current_list.insert(eq.latex_index[-1], ['^{', CURSOR, '}'])
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
    current_list.insert(eq.latex_index[-1], [r'\left(', CURSOR, r'\right.'])
    # Add new level to latex_index:
    eq.latex_index.append(1)

    return

def close_parens(eq):
    """
    called when ')' is typed explicitly or when the ) is navigated past using arrow keys.
    Need to figure out how to handle an attempt to delete just one of the parentheses
    """
    # TODO:
    # make sure this works properly.  Right now (x+1)/ doesn't come out right
    current_list = get_current_list(eq.latex_index, eq.latex)
    current_list[-1] = r'\right)'
    return
