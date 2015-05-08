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

def do_nothing(*args, **kwargs):
    pass

# These next few things set up key bindings that map keypresses to the functions that need to be
# called to handle them.
NO_MOD_KEY = 0
SHIFT = 1
ON_NUMPAD = 32

"""
TODO:
There's a cleaner way to do this, especially since it will get cluttered and shitty when adding all
the different modifier key names for cross platform support.  Consider changing it to something like,
'/' through 'equal' is the same below, then add the do_nothing's by checking the OS, and having a list 
of modifier keysym names for each OS.  Then use something like:

get(OS_specific_modifier_keysym)
for i in OS_specific_modifier_keysym:
    BINDINGS[i] = do_nothing
"""
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
    ('Shift_L', NO_MOD_KEY): do_nothing,
    ('Shift_R', NO_MOD_KEY): do_nothing,
    ('Control_L', NO_MOD_KEY): do_nothing,
    ('Control_R', NO_MOD_KEY): do_nothing,
    ('Alt_L', NO_MOD_KEY): do_nothing,
    ('Alt_R', NO_MOD_KEY): do_nothing,
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
        raise NoFunctionForKey('The key %s with state %s does not have an associated function' % (keysym, modifier))

class NoFunctionForKey(Exception):
    pass



        
