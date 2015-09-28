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
            expr.insert_after_cursor('\ ')
        expr.insert_after_cursor('}{')
    print str(expr)


def backspace(expr, *args):
    expr.backspace()


def delete(expr, *args):
    expr.delete_char()


def insert_char(expr, newkey):
    # It seems like there should be a cleaner way to do this, but I can't think of one.
    if newkey.char is '*':
        newkey.char = r'\cdot '
    expr.insert_at_cursor(newkey.char)



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


BINDINGS = {
    # Special characters:
    ('/', NO_MOD_KEY): insert_latex_command,
    ('slash', NO_MOD_KEY): insert_latex_command,
    ('^', SHIFT): insert_latex_command,
    ('asciicircum', SHIFT): insert_latex_command,  # Arch again
    ('_', SHIFT): insert_latex_command,
    ('underscore', SHIFT): insert_latex_command,
    ('\\', NO_MOD_KEY): do_nothing,
    ('backslash', NO_MOD_KEY): do_nothing,

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
"""
    # Operators:
    ('plus', SHIFT): insert_char,
    ('+', SHIFT): insert_char,
    ('*', SHIFT): insert_char,
    ('asterisk', SHIFT): insert_char,
    ('*', NO_MOD_KEY): insert_char,
    ('asterisk', NO_MOD_KEY): insert_char,
    ('*', ON_NUMPAD): insert_char,
    ('asterisk', ON_NUMPAD): insert_char,
    ('+', NO_MOD_KEY): insert_char,
    ('minus', NO_MOD_KEY): insert_char,
    ('=', NO_MOD_KEY): insert_char,
    ('=', ON_NUMPAD): insert_char,
    ('equal', NO_MOD_KEY): insert_char,
    ('plus', ON_NUMPAD): insert_char,
    ('minus', ON_NUMPAD): insert_char,
    ('equal', ON_NUMPAD): insert_char,

"""


def get_function_for(key):
    if (key.keysym, key.state) in BINDINGS:
        return BINDINGS[(key.keysym, key.state)]
    elif key.char is not None:
        return insert_char
    else:
        raise BindingsError('There is not an associated function for key ' + key.keysym + ' with state ' +
                            key.state)


class BindingsError(Exception):
    pass
