"""
(c) Daniel Hones 2014

MIT License


This file contains definitions for functions that PrettyMath objects use to handle keypresses and
the keybindings for those functions
"""

latex_functions = ['sin', 'cos', 'tan', 'cot', 'log', 'ln', 'lg',
                   'arcsin', 'arccos', 'arctan', 'sqrt']

def erase_cursor(node):
    return

def insert_char(expr, newkey):
    expr.add_string(newkey.keysym)
    return

def new_term(expr, newkey):
    
    return

def insert_frac(expr, newkey):
    new_item = LatexCommand(cmd='frac')
    new_item.arguments[0] = expr.active_item.data
    new_item.
    return new_item

def open_parens(expr, newkey):
    return

def close_parens(expr, newkey):
    return

def insert_superscript(expr, newkey):
    return

def insert_subscript(expr, newkey):
    return

def backslash(expr, newkey):
    return
    
BINDINGS = {('/', 0)      : insert_frac,
            ('(', 0)      : open_parens,  
            (')', 0)      : close_parens,
            ('^', 0)      : insert_superscript,
            ('_', 0)      : insert_subscript,
            ('\\', 0)     : backslash,
            ('plus', 0)   : new_term,
            ('minus', 0)  : new_term,
            ('equal', 0)  : new_term,
            ('plus', 32)  : new_term,
            ('minus', 32) : new_term,
            ('equal', 32) : new_term}

for keysym in 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890':
    self.BINDINGS[(keysym, 0)] = insert_char
    # 32 is the state for keys on the number pad (at least in OS X - need to check others)
    self.BINDINGS[(keysym, 32)] = insert_char
        
def new_binding(keysym, state, new_function):
    """
    Could have problems depending on where new_function is defined?
    """
    BINDINGS[(keysym, state)] = new_function
        
def get_function_for(keysym, state):
    # Returns the function that PrettyMath object needs to call to handle the new keypress.
    # Returns None if the keypress should be ignored
    # keysym and char are strings; state is an int
    if (keysym, state) in BINDINGS:
        return BINDINGS[(keysym, state)]
    else:
        # key doesn't have a binding
        return None


    
        
    
