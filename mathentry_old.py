"""
(c) Daniel Hones 2014

MIT License


This file defines the PrettyEquation class and MathEntryWidget class, along with some other utility 
functions and classes.

Might need to use copy.deepcopy in some places in the PrettyEquation class. Look into it:
https://docs.python.org/2/library/copy.html
"""

from translate_functions import *
from constants import *



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

# This is just a temporary class for testing the Observable class 
class Observer(object):
    def __init__(self):
        self.name = 'observer'
    def cb(self, *args):
        print "Updated: ", args[0]

class PrettyEquation(Observable):
    """
    This class has two main attributes: raw, which is a valid Python math expression, and latex
    which is that expression formatted to look nice in Latex.
    """

    def __init__(self):
        Observable.__init__(self)

        # Set up the rest of the class variables:
        self.reset()

        # This seems to be the only place to define these dictionaries:
        
        # This dictionary maps characters to functions that perform the required operation.
        # The functions it points to are defined in translate_functions.py 
        self.TRANSLATE_CHAR = {'/'      : insert_frac,
                               '('      : open_parens,
                               ')'      : close_parens,
                               '^'      : insert_superscript,
                               '_'      : insert_subscript,
                               r'\\'    : backslash}
        
        # This dictionary is for mapping keycodes to the right operation.
        # For example, left arrow, backspace, etc.  
        # This will need some work to make sure it works cross platform.
        # Use the keycode constants defined in mathentry_constants.py
        self.TRANSLATE_KEYCODE = {RIGHT : move_cursor,
                                  LEFT  : move_cursor,
                                  UP    : cursor_up,
                                  DOWN  : cursor_down }

        # This dictionary is for extending the LaTeX capabilities of this module.  It will allow
        # developers to add their own functions.  This will be checked before the default ones.
        # For example, someone could add functionality for a certain keyboard shortcut.  Need to figure
        # out the best way to format the keys.  Maybe keycodes and states?
        self.EXTENSIONS = {}


    def reset(self):
        """
        Reset the equation to a blank one
        """
        self.raw = []
        self.latex = [CURSOR]
        self.latex_index = [0]
        self.previous_keypress = ''
        self.running_list = []

    def add_keypress(self, newkey):
        """
        Takes a new event object representing a keypress.  Translates key and adds it to
        raw and latex in self.  Should it return an error?
        """

        if newkey.keycode in self.TRANSLATE_KEYCODE:
            self.TRANSLATE_KEYCODE[newkey.keycode](self, newkey.keycode)
            self.running_list = []
            self.notify_observers()
            return

        if newkey.keysym in IGNORE_THESE_KEYSYMS:
            return

        if newkey.keycode in IGNORE_THESE_KEYCODES:
            return

        # This won't always be an empty block:
        if newkey.keycode in SPECIAL_KEYCODES:
            return

        if newkey.char in self.TRANSLATE_CHAR:
            # Call the function needed to do some Latex formatting
            self.TRANSLATE_CHAR[newkey.char](self)
            self.running_list = []
            self.notify_observers()
            return

        
        # If there's nothing special that needs to be done with the new keypress, these next few lines
        # add the character to the latex equation at the current index, update running_list, 
        # previous_keypress (may not actually need that), and latex_index
        current_list = get_current_list(self.latex_index, self.latex)
        current_list.insert(self.latex_index[-1], newkey.char)
        self.latex_index[-1] += 1
        if newkey.char in SPECIAL_CHARS:
            self.running_list = []
        else:
            self.running_list.append(newkey.char)
        self.previous_keypress = newkey

        # Check to see if the end part of running_list is something meaningful in LaTeX:
        command = self.check_for_latex_command(''.join(self.running_list))
        if command:
            size = len(command)
            # Remove all the individual letters that spell the command
            del current_list[ self.latex_index[-1] - size : self.latex_index[-1] ]
            
            # Replace them with a single string element containing the LaTeX command
            current_list.insert(self.latex_index[-1] - size, LATEX_COMMANDS[command])

            # Reset running_list if it just inserted a function, otherwise make running_list
            # hold the current term.
            if command in FUNCTIONS:
                self.running_list = []
            else:
                del self.running_list[-size:]
                self.running_list.append(LATEX_COMMANDS[command])
            self.latex_index[-1] -= size - 1
               
            

        # This should be the last thing we do:
        self.notify_observers()

    def check_for_latex_command(self, string):
        """
        This function checks the string to see if it contains a LaTeX command.  It checks starting
        with the last two characters and stretches towards the beginning of the string one character
        at a time.
        """
        for i in range(2, len(string)+1):
            if string[-i:] in LATEX_COMMANDS:
                return string[-i:]
        return None
        
    def add_extension(self, key, function):
        self.EXTENSIONS[key] = function
        return

    def remove_extension(self,  key):
        del self.EXTENSIONS[key]
        return
    
    def get_latex(self):
        """
        Flattens and returns formatted equation as a string
        """
        return '$'+''.join(flatten(self.latex))+'$'

    def get_raw(self):
        """
        Converts the LaTeX expression into a valid Python one and returns it as a string
        """
        return