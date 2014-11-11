"""
(c) Daniel Hones 2014

MIT License


This file defines the PrettyEquation class and MathEntryWidget class, along with some other utility 
functions and classes.

Might need to use copy.deepcopy in some places in the PrettyEquation class. Look into it:
https://docs.python.org/2/library/copy.html
"""

from translate_functions import *
from mathentry_constants import *


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
    This class has two main attributes: raw, which is a valid Python math expression, and tex
    which is that expression formatted to look nice in TeX.
    """


    def __init__(self):
        Observable.__init__(self)

        # This dictionary maps characters to functions or lambdas that perform the required operation.
        # Apparently the function must be defined before they can be referenced here.
        self.TRANSLATE_CHAR = {r'/' : insert_frac,
                               r'(' : insert_parens}      
        
        # This dictionary is for mapping keycodes (or keysym?) to the right operation.
        # For example, left arrow, backspace, etc.  
        # This will need some work to make sure it works cross platform.
        self.TRANSLATE_KEYSYM = {}


        # Set up the rest of the class variables:
        self.reset()



    def reset(self):
        """
        Reset the equation to a blank one.  Good as new!
        """
        self.raw = []
        self.active_term = NEW_ACTIVE_TERM[:]
        self.tex = ['${', self.active_term, '}$']
        self.tex_index = [1,1]
        self.raw_index = 0
        self.previous_term = []
        self.previous_keypress = ''

    def add_keypress(self, newkey):
        """
        Takes a new event object representing a keypress.  Translates key and adds it to
        raw and tex in self.  Should it return an error?
        """
        # For debugging:
        print newkey.keycode    
        
        if newkey.keysym in IGNORE_THESE_KEYSYMS:
            return

        if newkey.keycode in IGNORE_THESE_KEYCODES:
            return

        if newkey.char in self.TRANSLATE_CHAR:
            self.TRANSLATE_CHAR[newkey.char](self)
            return

            

        # Check if we need to make a new term:
        if newkey.char in SPECIAL_CHARS:
            self.make_new_term(newkey.char)
            self.previous_keypress = newkey
            return
        
            
        
        # Not the real code:
        self.active_term.insert(self.tex_index[-1], newkey.char)
        self.raw.insert(self.raw_index, newkey.char)
        self.raw_index += 1
        self.tex_index[-1] += 1
        self.previous_keypress = newkey
        self.notify_observers()

    def make_new_term(self, char):
        """
        Makes a new active term at the same depth as the current one. For example 
        """
        # Remove cursor symbol and index to place in current active term:
        self.active_term.pop(self.tex_index.pop())

        # Put the current, just terminated active term into tex by VALUE, so that subsequent
        # changes to active_term no longer affect it:
        self.tex[self.tex_index[-1]] = self.active_term[:]

        # Insert the character:
        self.tex.insert( self.tex_index[-1] + 1, char )
        self.raw.insert( self.raw_index, char )
        self.raw_index += 1

        # Increment the next higher level index by 2
        self.tex_index[-1] += 2

        # Make new active term
        self.active_term = NEW_ACTIVE_TERM[:]
        self.tex.insert( self.tex_index[-1], self.active_term )

        # New active term index:
        self.tex_index.append(1)
        self.notify_observers()
        
        # Update previous keypress:
        
        
    def test_observe(self):
        """
        Just a temporary method to test the Observable mechanism
        """
        self.notify_observers()
        
    def get_tex(self):
        """
        Flattens and returns formatted equation as a string
        """
        return ''.join(flatten(self.tex))

    def get_raw(self):
        """
        Returns raw equation as a string
        """
        return ''.join(flatten(self.raw))
