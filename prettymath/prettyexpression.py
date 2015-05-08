"""
(c) Daniel Hones 2014

MIT License
"""

from latex_reference import LATEX_COMMANDS_WITH_ARGS, LATEX_COMMANDS_WITHOUT_ARGS
from containers import DataContainer
import bindings


class Observable(object):
    def __init__(self):
        self.observers = []
    def add_observer(self, callback):
        """
        An observer here is just a callback function to call when the variable changes 
        """
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
    CURSOR = '|'

    def __init__(self):
        super(PrettyExpression, self).__init__()
        initial_item = DataContainer(data=self.CURSOR)
        self.data_items = [initial_item]
        # Maybe implement the bindings so this works:
        
        # I'm torn as to whether it's better to keep track of the active item by pointing directly at the object
        # or by keeping indexes in each object that points to the position in the data list where the active object
        # or cursor is.
        self.active_item = initial_item

    def get_data(self):
        accumulated_data = []
        for i in self.data_items:
            accumulated_data.extend( i.get_data() )
        return accumulated_data
    
    def __str__(self):
        return ''.join(self.get_data())

    def get_latex(self):
        return '$' + str(self) + '$'

    def get_active_item(self):
        pass        
    
    def add_keypress(self, newkey):
        func = bindings.get_function_for(newkey.keysym, newkey.state)

        # TODO: change this to a try-catch block, by making get_function_for throw an exception
        # if there is no binding for a key.
        if func == None:
            print 'None returned'
            return
        else:
            func(self, newkey)
        
        # Just a placeholder as a reminder:
        self.check_for_latex_command('')

        # This should be the last thing we do:
        self.notify_observers()

    def new_binding(keysym, modifier, new_function):
        # This may turn out to be useless. But the idea is that a user can customize their bindings
        # for example maybe they want Ctrl+I to insert the integral sign or something.  They can
        # write their own function to handle it then add the binding here
        bindings.BINDINGS[(keysym, modifier)] = new_function

    def check_for_latex_command(self, string):
        """
        This function checks the string to see if it contains a LaTeX command.  It checks starting
        with the last two characters and stretches towards the beginning of the string one character
        at a time.
        At the moment it uses a simple approach, which seems to work fast enough. 
        """
        for i in range(2, len(string)+1):
            if string[-i:] in LATEX_COMMANDS_WITH_ARGS:
                # TODO:
                # Figure out what needs to be returned or done here and in the next block:
                pass
            elif string[-i:] in LATEX_COMMANDS_WITHOUT_ARGS:
                pass
        return None
