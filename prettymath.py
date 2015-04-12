"""
(c) Daniel Hones 2014

MIT License


This file defines the PrettyMath class and MathEntryWidget class, along with some other utility 
functions and classes.

The PrettyMath class uses a tree data structure to store the LaTeX formatted math.  The tree uses

right sibling.  'self' in the PrettyMath class definition always refers to the root of the tree, and 
the node that is currently being edited (contains the cursor) is self.active_node.  


TODO:
* Come up with solid plan for data structure (Atom class and others) and implement it.
* Finish and test insert_char method 
* Write unit tests
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
# and the character(s) to use to surround the first argument of the Latex command.  If three characters are given
# (like '_{}'), the first two go in front of the argument, the last one closes it.
LATEX_COMMANDS_WITH_ARGS = {
    '/': (2, 'active data'),
    '^': (1, '', '{}'),
    '_': (1, '', '{}'),
    'sqrt': (2, '', '[]'),
    'log': (2, '', '_{}'),
    'ln': (1, '', '{}'),
    'lg': (1, '', '{}')
}

# These commands (including Greek letters) take no arguments, just get a backslash before
# them to turn them into LaTeX commands.
LATEX_COMMANDS_NO_ARGS = [
    'sin',
    'cos',
    'tan',
    'cot',
    'sec',
    'csc',
    'arcsin',
    'arccos',
    'arctan'
]

greek_letters = [
    'alpha', 
    'beta',
    'gamma', 'Gamma',
    'delta', 'Delta',
    'epsilon', 'varepsilon',
    'zeta',
    'eta',
    'theta', 'vartheta', 'Theta',
    'iota',
    'kappa',
    'lambda', 'Lambda',
    'mu',
    'nu',
    'xi', 'Xi',
    'pi', 'Pi',
    'rho', 'varrho',
    'sigma', 'Sigma',
    'tau',
    'upsilon', 'Upsilon',
    'phi', 'varphi', 'Phi',
    'chi',
    'psi', 'Psi',
    'omega', 'Omega'
]

LATEX_COMMANDS_NO_ARGS.extend(greek_letters)
    
def insert_latex_command(expr, newkey):
    (num_args, special, arg_char) = LATEX_COMMANDS_WITH_ARGS[newkey.keysym]
    new_item = LatexCommand(cmd=newkey.keysym, args=num_args, first_arg_char=arg_char)
    if special == 'active data':
        new_item.arguments[0] = expr.active_item.data
    return new_item

def erase_cursor(expr):
    return

def insert_char(expr, newkey):
    # Not sure about this:
    expr.get_active_item().insert_at_cursor(newkey.char)
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

# These next few things set up key bindings that map keypresses to the functions that need to be
# called to handle them.
NUMPAD_STATE = (32,) # This is a tuple in case other OSes have other states for numpad keys.  32 is for OS X
BINDINGS = {
    ('/', 0)      : insert_latex_command,
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
    ('equal', 32) : new_term
}

for keysym in 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890':
    BINDINGS[(keysym, 0)] = insert_char # just insert the character like normal typing
    # NUMPAD_STATE is the state for keys on the number pad:
    for i in NUMPAD_STATE:
        BINDINGS[(keysym, i)] = insert_char
        
def new_binding(keysym, state, new_function):
    """
    I think maybe this should be defined inside the PrettyExpression class definition
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
    def __init__(self):
        pass
    def get_data(self):
        # Return as a list so that functions that call this one can .extend it to a list:
        return [self.data]

class Operand(object):
    def __init__(self, data=None):
        pass

class LatexCommand(object):
    def __init__(self, cmd='', args=0, first_arg_char=None):
        if cmd == '/':
            self.command = r'\frac' # This is just a special case
        else:
            self.command = cmd

        self.arguments = []
        self.num_arguments = len(self.arguments) # might not end up needing this
        for i in range(args):
            self.arguments.append( Argument() )
        self.arguments[0].set_enclosing_chars(first_arg_char) 
        return self

    def get_data(self):
        # This should be the LaTeX command itself, eg '\frac':
        accumulated_data = [self.command]
        # Then accumulate the data from the arguments:
        for arg in self.arguments:
            accumulated_data.extend( arg.get_data() )
        return accumulated_data

    def __str__(self):
        return ''.join( self.get_data() )


class Argument(Operand):
    def  __init__(self, enclosing_chars='{}'):
        super(Argument, self).__init__()
        self.enclosing_chars = enclosing_chars
        return self

    def set_enclosing_chars(self, chars):
        self.enclosing_chars = chars

    def get_data(self):
        return


class PrettyExpression(Observable):
    """
    This class has two main attributes: raw, which is a valid Python math expression, and latex
    which is that expression formatted to look nice in Latex.  It's sort of the container or root
    class for the operators and operands 
    """
    CURSOR = '|'

    def __init__(self):
        self.data_items = []
        self.active_index = 0
        self.root = self # not sure if this is needed
        return self

    def get_data(self):
        accumulated_data = []
        for i in self.data_items:
            accumulated_data.extend( i.get_data )
        return accumulated_data
    
    def __str__(self):
        return ''.join(self.get_data())

    def get_latex(self):
        return '$' + str(self) + '$'

    def get_active_item(self):
        pass        
    
    def add_keypress(self, newkey):
        # newkey.state is a bitfield that represents modifier keys pressed simultaneously with
        # the keysym.  It is 0 if there are no modifier keys:
        func = get_function_for(newkey)

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
            if string[-i:] in LATEX_COMMANDS_WITH_ARGS:
                # TODO:
                # Figure out what needs to be returned or done here and in the next block:
                pass
            elif string[-i:] in LATEX_COMMANDS_NO_ARGS:
                pass
        return None
        
