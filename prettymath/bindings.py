"""
(c) Daniel Hones 2014

MIT License
"""

from latex_reference import LATEX_COMMANDS_WITH_ARGS, LATEX_COMMANDS_WITHOUT_ARGS
import string
import containers

    
def insert_latex_command(expr, newkey):
    print 'got here'
    (num_args, special, arg_char) = LATEX_COMMANDS_WITH_ARGS[newkey.keysym]
    new_item = containers.LatexCommand(cmd=newkey.keysym, args=num_args, first_arg_char=arg_char)
    if special == 'active data':
        new_item.arguments[0] = expr.active_item.data
    return new_item

def erase_cursor(expr):
    return

def insert_char(expr, newkey):
    # It seems like there should be a cleaner way to do this, but I can't think of one.
    expr.active_item.insert_at_cursor(newkey.char)

def insert_operator(expr, newkey):
    return

def open_parens(expr, newkey):
    return

def close_parens(expr, newkey):
    return

def insert_superscript(expr, newkey):
    new_item = LatexCommand(cmd='^', args=1)
    return 

def insert_subscript(expr, newkey):
    return

def backslash(expr, newkey):
    return

def new_term():
    pass

# These next few things set up key bindings that map keypresses to the functions that need to be
# called to handle them.
NO_MOD_KEY = 0
SHIFT = 1
ON_NUMPAD = 32
BINDINGS = {
    ('/', NO_MOD_KEY) : insert_latex_command,
    ('slash', NO_MOD_KEY): insert_latex_command,
    ('(', SHIFT) : open_parens,  
    (')', SHIFT) : close_parens,
    ('^', SHIFT) : insert_latex_command,
    ('_', SHIFT) : insert_latex_command,
    ('\\', NO_MOD_KEY) : backslash,
    ('plus', SHIFT) : new_term,
    ('minus', NO_MOD_KEY) : new_term,
    ('equal', NO_MOD_KEY) : new_term,
    ('plus', ON_NUMPAD) : new_term,
    ('minus', ON_NUMPAD) : new_term,
    ('equal', ON_NUMPAD) : new_term,
}

for keysym in string.ascii_lowercase:
    BINDINGS[(keysym, NO_MOD_KEY)] = insert_char

for keysym in string.ascii_uppercase:
    BINDINGS[(keysym, SHIFT)] = insert_char

for keysym in string.digits:
    BINDINGS[(keysym, NO_MOD_KEY)] = insert_char
    BINDINGS[(keysym, ON_NUMPAD)] = insert_char


def get_function_for(keysym, modifier):
    if (keysym, modifier) in BINDINGS:
        return BINDINGS[(keysym, modifier)]
    else:
        return None





        
