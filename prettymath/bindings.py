"""
(c) Daniel Hones 2014

MIT License
"""

"""
TODO: Think about doing it this new way (need to consider the latex commands though):

Move all this shit into PrettyExpression (it will become simpler), and consider making
every key bound to insert_char, except for a dictionary of the special characters such
as backspace, delete, arrows, slash, and the like.  For Latex commands that need to be
inserted, just take the number arguments needed, generate a '{' on left_buffer, and '}'
on right_buffer, with another pair of them in the right_buffer if needed.  Then, make the
arrow key functions navigate through them as needed.
"""


from latex_reference import LATEX_COMMANDS_WITH_ARGS, LATEX_COMMANDS_WITHOUT_ARGS
import string
import containers


def insert_latex_command(expr, newkey):
    print "insert_latex_command called"
    (num_args, special, arg_char) = LATEX_COMMANDS_WITH_ARGS[newkey.keysym]
    if newkey.char is "/":
        expr.insert_at_cursor(r'\frac{')
    else:
        expr.insert_at_cursor(newkey.char + '{')

    expr.insert_after_cursor('}')
    for i in range(num_args - 1):
        if newkey.char is '/':
            # Just a stupid little hack to keep the computer from complaining
            expr.insert_after_cursor('.')
        expr.insert_after_cursor('}{')
    print str(expr)


def erase_cursor(expr):
    return


def backspace(expr, *args):
    expr.backspace()


def delete(expr, *args):
    expr.delete_char()


def insert_char(expr, newkey):
    # It seems like there should be a cleaner way to do this, but I can't think of one.
    expr.insert_at_cursor(newkey.char)


def open_parens(expr, newkey):
    return


def close_parens(expr, newkey):
    return


def insert_subscript(expr, newkey):
    return


def backslash(expr, newkey):
    pass


def do_nothing(*args, **kwargs):
    pass


def cursor_left(expr, *args):
    expr.move_cursor_left()


def cursor_right(expr, *args):
    expr.move_cursor_right()


# These next few things set up key bindings that map keypresses to the functions that need to be
# called to handle them.
NO_MOD_KEY = 0
SHIFT = 1
ON_NUMPAD = 32

"""
TODO:
There's a cleaner way to do this, especially since it will get cluttered when adding all
the different modifier key names for cross platform support.  Consider changing it to something like,
'/' through 'equal' is the same below, then add the do_nothing's by checking the OS, and having a list
of modifier keysym names for each OS.  Then use something like:

get(OS_specific_modifier_keysym)
for i in OS_specific_modifier_keysym:
    BINDINGS[i] = do_nothing
"""
BINDINGS = {
    # Special Latex characters:
    ('/', NO_MOD_KEY): insert_latex_command,
    ('slash', NO_MOD_KEY): insert_latex_command,
    ('^', SHIFT): insert_latex_command,
    ('asciicircum', SHIFT): insert_latex_command,  # Arch again
    ('_', SHIFT): insert_latex_command,
    ('underscore', SHIFT): insert_latex_command,
    # Other special characters:
    ('(', SHIFT): open_parens,
    (')', SHIFT): close_parens,
    ('parenleft', SHIFT): open_parens,  # This is what Arch calls ( and )
    ('parenright', SHIFT): close_parens,

    ('\\', NO_MOD_KEY): backslash,
    # Operators:
    ('plus', SHIFT): insert_char,
    ('+', SHIFT): insert_char,
    ('+', NO_MOD_KEY): insert_char,
    ('minus', NO_MOD_KEY): insert_char,
    ('=', NO_MOD_KEY): insert_char,
    ('=', ON_NUMPAD): insert_char,
    ('equal', NO_MOD_KEY): insert_char,
    ('plus', ON_NUMPAD): insert_char,
    ('minus', ON_NUMPAD): insert_char,
    ('equal', ON_NUMPAD): insert_char,
    # Modifier keys:
    ('Shift_L', NO_MOD_KEY): do_nothing,
    ('Shift_R', NO_MOD_KEY): do_nothing,
    ('Control_L', NO_MOD_KEY): do_nothing,
    ('Control_R', NO_MOD_KEY): do_nothing,
    ('Alt_L', NO_MOD_KEY): do_nothing,
    ('Alt_R', NO_MOD_KEY): do_nothing,
    # Control keys:
    ('BackSpace', NO_MOD_KEY): backspace,
    ('Delete', NO_MOD_KEY): delete,
    ('Left', NO_MOD_KEY): cursor_left,
    ('Right', NO_MOD_KEY): cursor_right,
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
        raise BindingsError('The key %s with state %s does not have an associated function' % (keysym, modifier))


class BindingsError(Exception):
    pass
