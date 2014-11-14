"""
(c) Daniel Hones 2014

MIT License


Defines constants for mathentry module
"""

import platform


def flatten(nested):
    """
    This function flattens a nested list or tuple so it can be joined as a string.  It always returns a list,
    regardless of the type of variable passed to it
    """
    result = []
    for i in nested:
        if type(i) in (list, tuple): 
            # Use extend because flatten returns a list
            result.extend(flatten(i))
        else:
            # Use append here because extend and += only work with iterables and if
            # this else block runs, i is not an iterable
            result.append(i)
    return result

# Define constants for keycodes across different platforms.
if platform.system() == 'Darwin':
    SHIFT       = (131074, 131076, 131330, 131332)
    SUPER       = (1048584, 1048592)
    CONTROL     = (262145, 270336)
    ALT         = (524320, 524352)
    CAPS_LOCK   = 65536
    HOME        = 65360
    END         = 65367
    PAGE_UP     = 7665452       # keysym 'Prior' in OS X
    PAGE_DOWN   = 7993133       # keysym 'Next' 
    BACKSPACE   = 3342463       # keysym 'BackSpace' 
    DELETE      = 7730984
    LEFT        = 8124162
    RIGHT       = 8189699
    UP          = 8320768
    DOWN        = 8255233
elif platform.system() == 'Linux':
    SHIFT       = (50, 62)
    SUPER       = 133
    CONTROL     = (37, 105)
    ALT         = (64, 108)
    CAPS_LOCK   = 66
    HOME        = 110
    END         = 115
    PAGE_UP     = 112           # keysym 'Prior' in Linux
    PAGE_DOWN   = 117           # keysym 'Next'
    BACKSPACE   = 22            # keysym 'BackSpace'
    DELETE      = 119
    LEFT        = 113
    RIGHT       = 114
    UP          = 111
    DOWN        = 116
    
    
    
# Define also for Windows


# Ignore these keys (may not be necessary)
# Maybe a better way is to check for special characters, then for special keys (like backspace, arrows0
# and then check if newkey.char (in mathentry.py) is a character, digit, or punctuation?
IGNORE_THESE_KEYCODES = flatten( (SHIFT, SUPER, CONTROL, ALT, CAPS_LOCK) )


# These are characters that that close the current active term and start a new one.
# These characters exist outside of the local term:
SPECIAL_CHARS = r'=+-*/(^'

# Keycodes that need something done with them:
SPECIAL_KEYCODES = {UP: '',
                    DOWN: '',
                    RIGHT: '',
                    LEFT: '',
                    BACKSPACE: '',
                    DELETE: ''}


# This is the list that is inserted when a new term is formed. The pipe symbol is used as a cursor
NEW_ACTIVE_TERM = ['{', '|', '}']

# Once get a complete list of keycodes for windows and linux, can erase this.  These are Linux:
IGNORE_THESE_KEYSYMS = ['Shift_L', 'Shift_R', 'Alt_L', 'Alt_R', 'Control_L', 'Control_R']

# This dictionary maps LaTeX commands to what to replace them with in the formatted equation.
# This allows for example, typing 'pi' to translate to '\pi'.  Not sure how many of these I should support
# The space after the command makes it possible to have consecutive LaTeX commands without throwing an error
LATEX_COMMANDS = {'pi'          : r'\pi ',
                  'omega'       : r'\omega ',
                  'epsilon'     : r'\epsilon ',
                  'sin'         : r'\sin ',
                  'cos'         : r'\cos ',
                  'tan'         : r'\tan ',
                  'cot'         : r'\cot ',
                  'sec'         : r'\sec ',
                  'csc'         : r'\csc ',
                  'log'         : r'\log ',
                  'ln'          : r'\ln ',
                  'lg'          : r'\lg ',
                  'cross'       : r'\cross',            # maybe have a keyboard shortcut for this
                  'infty'       : r'\infty '}

FUNCTIONS = ('sin', r'\sin ',
             'cos', r'\cos ',
             'tan', r'\tan ',
             'cot', r'\cot ',
             'sec', r'\sec ',
             'csc', r'\csc ',
             'log', r'\log ',
             'ln', r'\ln ',
             'lg', r'\lg ',
             'cross', r'\cross ')
