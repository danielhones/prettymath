"""
(c) Daniel Hones 2014

MIT License
"""

"""
TODO:

Start cleaning up the awful bindings mess.  Probably easy enough to start it from scratch, since
it's now simplified a bit, so take the hatchet to it.  Read up on "The Craft of Text Editing" to
see if there are any ideas to help with the architecture.

Get subscript and superscript working.

Get frac working at least halfway, where you can type '/' as a new term and it creates a new fraction.
Make up and down arrow keys work with it.

Once things are going in the right direction, get rid of bindings.py and containers.py

Start implementing the latex_to_python translater (check to see if there's already something that exists
for this)
"""


from collections import deque
from latex_reference import LATEX_COMMANDS_WITH_ARGS, LATEX_COMMANDS_WITHOUT_ARGS, CURSOR
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
        # These lines can be erased soon:
        # self.active_item = DataContainer(data=CURSOR)
        # self._data_items = [self.active_item]

    @property
    def data(self):
        accumulated_data = []
        for i in self._data_items:
            accumulated_data.extend(i.data)
        return accumulated_data

    @data.setter
    def data(self, items):
        if type(items) is not list:
            self._data_items = [items]
        else:
            self._data_items = items

    def append(self, item):
        self._data_items.append(item)

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

    def reset(self):
        """Reset the object to an empty state, containing only the cursor"""
        self.left_buffer = deque()
        self.right_buffer = deque()

    def add_keypress(self, newkey):
        try:
            func = bindings.get_function_for(newkey.keysym, newkey.state)
            func(self, newkey)
        except bindings.BindingsError as error:
            print error

        # print 'PrettyExpression:', str(self.latex)
        self.check_for_latex_command()
        self.notify_observers()

    def insert_at_cursor(self, char):
        self.left_buffer.append(char)

    def backspace(self):
        # TODO: write a decorator for this pattern
        try:
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

    def check_for_latex_command(self):
        """
        Check this object for a recently-typed LaTeX command and if there is one, parse it and
        add it to the data structure
        """
        pass
