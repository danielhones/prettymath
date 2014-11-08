"""
(c) Daniel Hones 2014

MIT License


Here will go the functions for parsing the raw string into latex-ified typeset math
"""

def flatten(a_list):
    """
    This function flattens a nested list so it can be joined as a string
    """
    result = []
    for i in a_list:
        if type(i) is list:
            result.extend(flatten(i))
        else:
            result.extend(i)
    return result

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
    This class has two main attributes: raw_eq, which is a valid Python math expression, and tex_eq
    which is that expression formatted to look nice in TeX.
    """
    # These are characters that that close the current active term and start a new one.
    # These characters exist outside of the local term:
    NEW_TERM_CHARS = r'=+-*('
    # This is the list that is inserted when a new term is formed. The pipe symbol is used as a cursor
    NEW_ACTIVE_TERM = ['{', '|', '}']
    IGNORE_KEYS = ['Shift_L', 'Shift_R', 'Alt_L', 'Alt_R', 'Control_L', 'Control_R',
                   'Tab'] 
                   
                   
    # This dictionary maps characters to functions or lambdas that perform the required operation.
    # Apparently the function must be defined before they can be referenced here.
#    TRANSLATE_CHAR = {r'/' : insert_frac(),
#                      r'(' : insert_parens()}      
    # This dictionary is for mapping keycodes (or keysym?) to the right operation.
    # For example, left arrow, backspace, etc.
    TRANSLATE_KEYCODE = {}

    def __init__(self):
        Observable.__init__(self)
        self.reset()

    def reset(self):        
        self.raw_eq = []
        self.active_term = self.NEW_ACTIVE_TERM[:]
        self.tex_eq = ['${', self.active_term, '}$']
        self.tex_eq_index = [1,1]
        self.raw_eq_index = 0

    def add_keypress(self, newkey):
        """
        Takes a new event object representing a keypress.  Translates key and adds it to
        raw_eq and tex_eq in self.  Should it return an error?
        """
        if newkey.keysym in self.IGNORE_KEYS:
            return

        # First check if we need to make a new term:
        if newkey.char in self.NEW_TERM_CHARS:
            self.make_new_term(newkey.char)
            return

        # Not the real code:
        self.active_term.insert(self.tex_eq_index[-1], newkey.char)
        self.raw_eq.insert(self.raw_eq_index, newkey.char)
        self.raw_eq_index += 1
        self.tex_eq_index[-1] += 1
        self.notify_observers()

    def make_new_term(self, char):
        """
        Makes a new active term at the same depth as the current one. For example 
        """
        # Remove cursor symbol and index to place in current active term:
        self.active_term.pop(self.tex_eq_index.pop())
        # Put the current, just terminated active term into tex_eq by VALUE, so that subsequent
        # changes to active_term no longer affect it:
        self.tex_eq[self.tex_eq_index[-1]] = self.active_term[:]
        # Insert the character:
        self.tex_eq.insert( self.tex_eq_index[-1] + 1, char )
        self.raw_eq.insert( self.raw_eq_index, char )
        self.raw_eq_index += 1
        # Increment the next higher level index by 2
        self.tex_eq_index[-1] += 2
        # Make new active term:
        self.active_term = self.NEW_ACTIVE_TERM[:]
        self.tex_eq.insert( self.tex_eq_index[-1], self.active_term )
        # New active term index:
        self.tex_eq_index.append(1)
        self.notify_observers()
        
        
    def test_observe(self):
        """
        Just a temporary method to test the Observable mechanism
        """
        self.notify_observers()
        
    def get_tex_eq(self):
        """
        Flattens and returns formatted equation as a string
        """
        return ''.join(flatten(self.tex_eq))

    def get_raw_eq(self):
        """
        Returns raw equation as a string
        """
        return ''.join(self.raw_eq)
