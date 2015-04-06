"""
(c) Daniel Hones 2014

MIT License


This file defines the PrettyMath class and MathEntryWidget class, along with some other utility 
functions and classes.

The PrettyMath class uses a tree data structure to store the LaTeX formatted math.  The tree uses

right sibling.  'self' in the PrettyMath class definition always refers to the root of the tree, and 
the node that is currently being edited (contains the cursor) is self.active_node.  


TODO:
* Write unit tests
* Figure out where error handling is needed and write it (maybe ensure that data is always a list of strings?).
"""


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


"""
The following functions and variables are for mapping keypresses to the functions that need to be called
to handle them.
"""
# This dictionary maps LaTeX commands to the number of arguments each one takes, and a special instruction,
# and the character to use to surround the first argument of the Latex command 
latex_commands = {
    '/': (2, 'active data'),
    '^': (1, '', '{}'),
    '_': (1, '', '{}'),
    'sqrt': (2, '', '[]'),
    'sin': (0, '', '{}'),
    'cos': (0, '', '{}'),
    'tan': (0, '', '{}'),
    'cot': (0, '', '{}'),
    'sec': (0, '', '{}'),
    'csc': (0, '', '{}'),
    'arcsin': (0, '', '{}'),
    'arccos': (0, '', '{}'),
    'arctan': (0, '', '{}'),
    'log': (2, '', '_'),
    'ln': (1, '', '{}'),
    'lg': (1, '', '{}')
}
    
def insert_latex_command(expr, newkey):
    (num_args, special, arg_char) = latex_command_arguments[newkey.keysym]
    new_item = LatexCommand(cmd=newkey.keysym, args=num_args, first_arg_char=arg_char)
    if special == 'active data':
        new_item.arguments[0] = expr.active_item.data
    return new_item

def erase_cursor(expr):
    return

def insert_char(expr, newkey):
    expr.add_string(newkey.keysym)
    return

def insert_operator(expr, newkey):
    return

def open_parens(expr, newkey):
    return

def close_parens(expr, newkey):
    return

def insert_superscript(expr, newkey):
    new_item = LatexCommand(cmd='^', args=1)
    return 

def insert_subscript(expr, newkey):
    return

def backslash(expr, newkey):
    return
    
BINDINGS = {('/', 0)      : insert_latex_command,
            ('(', 0)      : open_parens,  
            (')', 0)      : close_parens,
            ('^', 0)      : insert_latex_command,
            ('_', 0)      : insert_latex_command,
            ('\\', 0)     : backslash,
            ('plus', 0)   : new_term,
            ('minus', 0)  : new_term,
            ('equal', 0)  : new_term,
            ('plus', 32)  : new_term,
            ('minus', 32) : new_term,
            ('equal', 32) : new_term}

for keysym in 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890':
    BINDINGS[(keysym, 0)] = insert_char
    # 32 is the state for keys on the number pad (at least in OS X - need to check others)
    BINDINGS[(keysym, 32)] = insert_char
        
def new_binding(keysym, state, new_function):
    """
    Could have problems depending on where new_function is defined?
    """
    BINDINGS[(keysym, state)] = new_function
        
def get_function_for(keysym, state):
    # Returns the function that PrettyMath object needs to call to handle the new keypress.
    # Returns None if the keypress should be ignored
    # keysym and char are strings; state is an int
    if (keysym, state) in BINDINGS:
        return BINDINGS[(keysym, state)]
    else:
        # key doesn't have a binding
        return None

class Operator(object):
    pass

class LatexCommand(object):
    pass

class PrettyMath(Observable):
    """
    This class has two main attributes: raw, which is a valid Python math expression, and latex
    which is that expression formatted to look nice in Latex.  It's sort of the container or root
    class for the operators and operands 
    """
    CURSOR = '|'

    def __init__(self):
        return self
        
    def __str__(self):
        return
    
    def add_keypress(self, newkey):
        # newkey.state is a bitfield that represents modifier keys pressed simultaneously with
        # the keysym.  It is 0 if there are no modifier keys:
        func = self.binding_map.get_function_for(newkey)

        if func == None:
            return
        else:
            func(self, newkey)
        
        # Just a placeholder as a reminder:
        self.check_for_latex_command('')

        # This should be the last thing we do:
        self.notify_observers()


    def check_for_latex_command(self, string):
        """
        This function checks the string to see if it contains a LaTeX command.  It checks starting
        with the last two characters and stretches towards the beginning of the string one character
        at a time.
        At the moment it uses a simple approach, which seems to work fast enough. 
        """
        for i in range(2, len(string)+1):
            if string[-i:] in LATEX_COMMANDS:
                return string[-i:]
        return None
        
