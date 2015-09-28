"""
(c) Daniel Hones 2014

MIT License
"""

"""
TODO: Clean up the awful bindings mess.

Probably easy enough to start it from scratch, since it's now simplified a bit, so take the hatchet to it.
Read up on "The Craft of Text Editing" to see if there are any ideas to help with the architecture.  It might
be simplest to first check to see if the keysym is in a dictionary of special keys (arrows, backspace, etc)
and if not, just look up by key.character.  That would be best for crossplatform I think since there's no
stupid "^" being "asciicircum" kind of stuff.  Once things are going in the right direction, get rid of bindings.py
and containers.py


TODO: Implement the latex_to_python translater
TODO: Implement left and right parentheses
TODO: See if it's possible to make subscripts a little smaller font and add a little extra space to the right of them
TODO: Implement Latex command and greek letter substitution (like sin, cos, sigma, etc).  Think about making this
      algorithm match as much as possible, rather than as soon as possible, that way you could type "epsilon" and
      get "\epsilon" instead of "e\psi lon"
TODO: Look into altering matplotlib.mathtext to custom render the cursor so it doesn't move characters out of the way
      as you navigate through the text, and adjust certain things (like make "=" and "+" a little smaller, make
      nested fracs, superscripts, and the like not diminish in size so quickly (or maybe it's just better to set a
      larger font size on the renderer canvas).  Also see about making the cursor character shorter vertically, so
      that it doesn't throw off vertical spacing of elements as it moves through the expression.
TODO: \frac{}{} with empty arguments makes the renderer complain.  See if there's a way to fix it.
"""


from collections import deque
from latex_translate import latex_to_python
from latex_reference import CURSOR, LATEX_COMMAND_FUNCTIONS, LATEX_COMMANDS_WITHOUT_ARGS
import bindings


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
    This class has two main attributes: raw, which is a valid Python math expression, and latex
    which is that expression formatted to look nice in Latex.  It's sort of the container or root
    class for the operators and operands.

    This class uses a split buffer (consisting of self.left_buffer and self.right_buffer) data structure
    to contain the LaTeX math expression.  The split is at the cursor.
    """

    def __init__(self, data=None):
        super(PrettyExpression, self).__init__()
        self.cursor = CURSOR
        self.reset()  # initialize left_buffer and right_buffer

    def reset(self):
        """Reset the object to an empty state, containing only the cursor"""
        # Strictly speaking, only the right buffer needs to be a deque since it is the only one
        # that will need to push and pop its 0 index.
        self.left_buffer = deque()
        self.right_buffer = deque()
        self.running_string = []
        self.notify_observers()

    @property
    def latex(self):
        return '$' + str(self) + '$'

    @property
    def cursorless_latex(self):
        return '$' + self.cursorless_str + '$'

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
        try:
            func = bindings.get_function_for(newkey.keysym, newkey.state)
            func(self, newkey)
        except bindings.BindingsError as error:
            print error

        print 'PrettyExpression:', str(self)
        self.notify_observers()

    def insert_at_cursor(self, char):
        self.left_buffer.append(char)
        self._check_for_latex_command()

    def insert_after_cursor(self, char):
        self.right_buffer.appendleft(char)

    def backspace(self):
        # TODO: make this handle backspacing over curly braces.  Maybe make it move into the curly braces
        #       and erase the next character?  Right now it throws an error.
        try:
            if self.left_buffer[-1] == '}':
                self.move_cursor_left()
            if self.left_buffer[-1] == '{':
                self.right_buffer.popleft()
                self.left_buffer.pop()
            self.left_buffer.pop()
        except IndexError:
            pass

    def delete_char(self):
        try:
            self.right_buffer.popleft()
        except IndexError:
            pass

    def move_cursor_left(self):
        try:
            self.right_buffer.appendleft(self.left_buffer.pop())
        except IndexError:
            pass

    def move_cursor_right(self):
        try:
            self.left_buffer.append(self.right_buffer.popleft())
        except IndexError:
            pass

    def _check_for_latex_command(self):
        """
        Check this object for a recently-typed LaTeX command and if there is one, parse it and
        add it to the data structure
        """
        # This still has the problem that it terminates as soon as possible, for example it will
        # match the 'sin' part of 'sinh' first, making it impossible to get 'sinh'
        # TODO: Change this so it deals with the problem of prematurely writing Latex commands
        TERMINATING_CHARS = r'\*+-=^_{}()'
        index = len(self.left_buffer) - 1
        next_char = self.left_buffer[index][0]
        check_pieces = deque(next_char)

        while (index >= 0) and (next_char not in TERMINATING_CHARS):
            check_string = ''.join(check_pieces)
            if check_string in LATEX_COMMAND_FUNCTIONS:
                command = '\\' + check_string + ' '
                self._replace_in_left_buffer(command, len(check_pieces))
                self.insert_at_cursor('(')
                self.insert_after_cursor(')')
            elif check_string in LATEX_COMMANDS_WITHOUT_ARGS:
                command = '\\' + check_string + ' '
                self._replace_in_left_buffer(command, len(check_pieces))
            index -= 1
            next_char = self.left_buffer[index][0]
            check_pieces.appendleft(next_char)

    def _replace_in_left_buffer(self, string, num_pieces):
        for i in range(num_pieces):
            self.left_buffer.pop()
        self.insert_at_cursor(string)
