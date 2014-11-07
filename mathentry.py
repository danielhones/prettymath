"""
Here will go the functions for parsing the raw string into latex-ified typeset math
"""

import string

TRANSLATIONS = {'/': ['\frac']}
CHARACTERS = string.letters + string.digits
NEW_TERM_CHARS = r'+-*/^'

class PrettyEquation(object):
    def __init__(self):
        self.raw_eq = ''
        self.tex_eq = ['${','}$']
        self.active_term = '{}'
        # Think very hard about the best way to do the cursor index:
        self.cursor_index = [0,2]
            
    def add_keypress(newkey):
        """
        Takes a new event object representing a keypress.  Translates key and adds it to
        raw_eq and tex_eq in self.  Should it return an error?
        """
        if newkey.char in CHARACTERS:
            self.raw_eq += newkey.char
            #self.active_term += 
            #self.tex_eq
            self.cursor_index[-1] += 1
            
        
    
