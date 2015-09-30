"""
(c) Daniel Hones 2014

MIT License
"""

"""
TODO: Clean up the awful bindings mess.
TODO: Look into defining and using custom font to custom render the cursor so it doesn't move characters out of the way
      as you navigate through the text, and adjust certain things (like make "=" and "+" a little smaller, make nested
      fracs, superscripts, and the like not diminish in size so quickly (or maybe it's just better to set a larger font
      size on the renderer canvas).  Also see about making the cursor character shorter vertically, so that it doesn't
      throw off vertical spacing of elements as it moves through the expression.
"""


from collections import deque
from latex_translate import latex_to_python
from latex_reference import CURSOR, LATEX_COMMAND_FUNCTIONS, LATEX_COMMANDS_WITHOUT_ARGS, LATEX_COMMANDS_WITH_ARGS


def do_nothing(*args, **kwargs):
    pass


NO_MOD_KEY = 0
SHIFT = 1
CTRL = 4
ALT = 8
ON_NUMPAD = 32
SUPER = 64
SPACE_CHAR = r'\ '
TIMES_DOT = r'\cdot '
# These characters reset the command_buffer that tracks typed latex commands
COMMAND_TERMINATING_CHARS = [i for i in '\*+-=^_{}()/']
COMMAND_TERMINATING_CHARS.append(TIMES_DOT)
# TODO: Think about switching to using XOR to bind keys with multiple mod key states
IGNORED_KEYS = {
    ('\\', NO_MOD_KEY): do_nothing,
    ('{', SHIFT): do_nothing,
    ('}', SHIFT): do_nothing,
    ('{', NO_MOD_KEY): do_nothing,
    ('}', NO_MOD_KEY): do_nothing,
    ('Shift_L', NO_MOD_KEY): do_nothing,
    ('Shift_R', NO_MOD_KEY): do_nothing,
    ('Control_L', NO_MOD_KEY): do_nothing,
    ('Control_R', NO_MOD_KEY): do_nothing,
    ('Alt_L', NO_MOD_KEY): do_nothing,
    ('Alt_R', NO_MOD_KEY): do_nothing,
}


class Observable(object):
    def __init__(self):
        self.observers = []

    def add_observer(self, callback):
        self.observers.append(callback)

    def notify_observers(self):
        for callback in self.observers:
            callback(self)


class PrettyExpression(Observable):
    """
    TODO: make this docstring actually useful.

    This class uses a split buffer (consisting of self.left_buffer and self.right_buffer) data structure
    to contain the LaTeX math expression.  The split is at the cursor.
    """
    def __init__(self, data=None):
        super(PrettyExpression, self).__init__()
        self.cursor = CURSOR
        self.left_buffer = deque()
        self.right_buffer = deque()
        self.command_buffer = []
        self.BINDINGS = {
            ('/', NO_MOD_KEY): self._make_frac,
            ('^', SHIFT): self._insert_latex_command,
            ('^', NO_MOD_KEY): self._insert_latex_command,
            ('_', SHIFT): self._insert_latex_command,
            # Control keys:
            ('BackSpace', NO_MOD_KEY): self._backspace,
            ('Delete', NO_MOD_KEY): self._delete,
            ('Left', NO_MOD_KEY): self._move_cursor_left,
            ('Right', NO_MOD_KEY): self._move_cursor_right,
            ('Up', NO_MOD_KEY): do_nothing,
            ('Down', NO_MOD_KEY): do_nothing,
        }
        self.BINDINGS.update(IGNORED_KEYS)

    def reset(self):
        """Reset the object to an empty state, containing only the cursor"""
        # Strictly speaking, only the right buffer needs to be a deque since it is the only one
        # that will need to push and pop its 0 index.
        self.left_buffer.clear()
        self.right_buffer.clear()
        self.command_buffer = []
        self.notify_observers()

    @property
    def latex(self):
        return '$' + str(self) + '$'

    def __str__(self):
        return self._before_cursor + self.cursor + self._after_cursor

    @property
    def cursorless_str(self):
        return self._before_cursor + self._after_cursor

    @property
    def _before_cursor(self):
        return ''.join(self.left_buffer)

    @property
    def _after_cursor(self):
        return ''.join(self.right_buffer)

    @property
    def expression(self):
        return latex_to_python(self.cursorless_str)

    def add_keypress(self, newkey):
        self.newkey = newkey
        try:
            key_action = self._get_action_for_key()
        except BindingsError as error:
            print error
        key_action()
        self._check_for_latex_command()
        print 'PrettyExpression:', str(self)
        self.notify_observers()

    def _get_action_for_key(self, key=None):
        if key is None:
            key = self.newkey
        # Check to see if the key has a special binding first:
        if (key.char, key.state) in self.BINDINGS:
            return self.BINDINGS[(key.char, key.state)]
        elif (key.keysym, key.state) in self.BINDINGS:
            return self.BINDINGS[(key.keysym, key.state)]
        elif key.char is not None:
            # Otherwise, just insert the character if there is one:
            return self._insert_at_cursor
        else:
            raise BindingsError('There is not an associated function for key ' + key.keysym + ' with state ' +
                                key.state)

    def _insert_at_cursor(self, char=None):
        if char is None:
            char = self.newkey.char
        if char is '*':
            char = TIMES_DOT
        # Clean up blank placeholder:
        if len(self.right_buffer) > 0 and self.right_buffer[0] == SPACE_CHAR:
            self.right_buffer.popleft()
        self.left_buffer.append(char)

    def _insert_after_cursor(self, char=None):
        if char is None:
            char = self.newkey.char
        if type(char) in (tuple, list):
            self.right_buffer.extendleft(char[::-1])
        else:
            self.right_buffer.appendleft(char)

    def _backspace(self):
        # TODO: make this handle backspacing over curly braces.  Maybe make it move into the curly braces
        #       and erase the next character?  Right now it throws an error.  Maybe write a method that cleans
        #       unmatched curly braces and call it whenever _delete or _backspace are called
        self.command_buffer = []
        try:
            if self.left_buffer[-1] == '}':
                self._move_cursor_left()
            if self.left_buffer[-1] == '{':
                self.right_buffer.popleft()
                self.left_buffer.pop()
            self.left_buffer.pop()
        except IndexError:
            pass

    def _delete(self):
        self.command_buffer = []
        try:
            self.right_buffer.popleft()
        except IndexError:
            pass

    def _move_cursor_left(self):
        try:
            self.right_buffer.appendleft(self.left_buffer.pop())
        except IndexError:
            pass

    def _move_cursor_right(self):
        try:
            self.left_buffer.append(self.right_buffer.popleft())
        except IndexError:
            pass

    def _make_frac(self):
        NEW_TERM_CHARS = '+-'
        BEGIN_FRAC = r'\frac{'
        SEPARATOR = '}{'
        END_FRAC = '}'
        if (len(self.left_buffer) > 0 and self.left_buffer[-1] in NEW_TERM_CHARS) or \
           (len(self.left_buffer) == 0):
            # This means '/' was pressed in a new term, there's no numerator or denominator
            self._insert_at_cursor(BEGIN_FRAC)
            self._insert_after_cursor([SEPARATOR, SPACE_CHAR, END_FRAC])
        else:
            # This means '/' was pressed after a numerator was entered, we need to find the numerator,
            # put '\frac{' before it, '}{' after it but before the cursor, and '}' after the cursor
            temp_buffer = [self.left_buffer.pop()]
            while len(self.left_buffer) > 0 and temp_buffer[-1] not in NEW_TERM_CHARS:
                temp_buffer.append(self.left_buffer.pop())
            self.left_buffer.extend([BEGIN_FRAC] + temp_buffer[::-1] + [SEPARATOR])
            self._insert_after_cursor(END_FRAC)

    def _insert_latex_command(self, command=None):
        if command is None:
            command = self.newkey.char
            delimiters = LATEX_COMMANDS_WITH_ARGS[command]
            cmd_first_d = command + delimiters[0]
        else:
            delimiters = LATEX_COMMANDS_WITH_ARGS[command]
            cmd_first_d = '\\' + command + delimiters[0]
        self._insert_at_cursor(cmd_first_d)
        for d in delimiters[:0:-1]:
            self._insert_after_cursor(d)

    def _check_for_latex_command(self):
        """
        Check this object for a recently-typed LaTeX command and if there is one, parse it and
        add it to the data structure
        """
        # TODO: Figure out a non-dumb way to do this
        pass

    def _replace_in_left_buffer(self, string, num_pieces):
        for i in range(num_pieces):
            self.left_buffer.pop()
        self._insert_at_cursor(string)


class PrettyExpressionError(Exception):
    pass


class BindingsError(Exception):
    pass
