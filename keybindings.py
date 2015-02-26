"""
(c) Daniel Hones 2014

MIT License


This file contains definitions for functions that PrettyMath objects use to handle keypresses.
"""

            

def insert_char(node, newkey):
    # node is the active node of the PrettyMath object, char is the new character to add to it
    node.data.insert(node.cursor_index, newkey.char)
    node.running_list.append(newkey.char)
    node.cursor_index += 1
    return

def new_term(node, newkey):
    # When making a new subtree, the data passed to it must be a LIST or else a type error
    # is thrown in walk_tree
    del node.data[node.root.cursor_index] 
    node.active_node = node.insert_child([newkey.char, node.CURSOR])
    node.root.cursor_index = len(node.active_node.data) - 1 
    return

def insert_frac(node, newkey):
    return

def open_parens(node, newkey):
    return

def close_parens(node, newkey):
    return

def insert_superscript(node, newkey):
    return

def insert_subscript(node, newkey):
    return

def backslash(node, newkey):
    return
    

# This is for mapping keypresses to their functions
BINDINGS = {'/'         : insert_frac,
            '('         : open_parens,
            ')'         : close_parens,
            '^'         : insert_superscript,
            '_'         : insert_subscript,
            r'\\'       : backslash,
            'plus'      : new_term, # need to make sure these are same crossplatform
            'minus'     : new_term,
            'equal'     : new_term}

def get_function_for(keysym, char, state):
    # Returns the function that PrettyMath object needs to call to handle the new keypress.
    # Returns None if the keypress should be ignored
    # keysym and char are strings; state is an int
    if keysym in BINDINGS:
            return BINDINGS[keysym]
    elif keysym == char and state == 0:
            # This is simplistic and needs to be checked that it's always the case (crossplatform),
            # but for now, the assumption is that keysym == char if and only if the keysym is a printable
            # character (numbers, letters, space, etc).  In other words, it doesn't need special handling
            # like arrow keys or backspace.  So, after checking for special case characters (ie ^ or /),
            # it falls through to this case: 
            return insert_char
    # Or if it can be ignored:
    else:
        return None


    
        
    
