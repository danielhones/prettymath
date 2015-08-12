"""
(c) Daniel Hones 2014

MIT License
"""

from latex_reference import LATEX_COMMANDS_WITH_ARGS, LATEX_COMMANDS_WITHOUT_ARGS, CURSOR
from containers import DataContainer
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
    class for the operators and operands
    """
    def __init__(self):
        super(PrettyExpression, self).__init__()
        self.active_item = DataContainer(data=CURSOR)
        self._data_items = [self.active_item]

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

    def __str__(self):
        return ''.join(self.data)

    @property
    def latex(self):
        return '$' + str(self) + '$'

    def reset(self):
        """Reset the object to an empty state, containing only the cursor"""
        # TODO:
        # Make sure that this doesn't leak memory due to the created DataContainer objects
        # referencing each other.
        self.active_item = DataContainer(data=CURSOR)
        self._data_items = [self.active_item]

    def add_keypress(self, newkey):
        try:
            func = bindings.get_function_for(newkey.keysym, newkey.state)
            func(self, newkey)
        except bindings.BindingsError as error:
            print error

        print 'PrettyExpression:', str(self.latex)
        self.check_for_latex_command()
        self.notify_observers()

    def new_binding((keysym, modifier), new_function):
        # This may turn out to be useless. But the idea is that a user can customize their bindings,
        # for example maybe they want Ctrl+I to insert the integral sign.  They can write their own
        # function to handle it then add the binding here
        bindings.BINDINGS[(keysym, modifier)] = new_function

    def check_for_latex_command(self):
        """
        Check this object for a recently-typed LaTeX command and if there is one, parse it and
        add it to self._data_items
        """
        # TODO:
        # There is a problem with doing it this way because it is impossible to type "cosh"
        # or anything like that where the first portion of the command is the same as another
        # LaTeX command, since the program will match "cos" first and turn "cosh" into
        # "{\cos}h".  So we need to check if the previous string, combined with an already parsed
        # Latex command matches another Latex command.
        # It also fails on things like "epsilon" which becomes "e{\psi}lon"
        check = ''
        index = len(self.active_item.data) - 2
        while self._not_a_command(check) and index >= 0:
            check = ''.join(self.active_item.data[index:-1])
            if check in LATEX_COMMANDS_WITH_ARGS:
                # TODO:
                # Determine what needs to be here
                print "Command found:", check
            elif check in LATEX_COMMANDS_WITHOUT_ARGS:
                self._replace_with_command(check)
            index -= 1

    def _not_a_command(self, x):
        return not (x in LATEX_COMMANDS_WITH_ARGS or x in LATEX_COMMANDS_WITHOUT_ARGS)

    def _replace_with_command(self, command):
        command_start = len(self.active_item.data) - (len(command) + 1)
        command_end = -1
        # We need to access _data_items like this since active_item.data is an @property,
        # so we can't alter it directly.  Seems like there should be a cleaner way
        del self.active_item._data_items[command_start:command_end]
        self.active_item.cursor_index -= len(command)
        self.active_item.insert_at_cursor('{\\' + command + '}')
