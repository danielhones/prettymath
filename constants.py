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
    PAGE_UP     = 7665452       # keysym is 'Prior' in OS X
    PAGE_DOWN   = 7993133       # keysym is 'Next' in OS X
    BACKSPACE   = 3342463       # keysym is 'BackSpace' in OS X        
    DELETE      = 7730984
    LEFT        = 8124162
    RIGHT       = 8189699
    UP          = 8320768
    DOWN        = 8255233
    

# Define also for Windows and Linux here:


# Ignore these keys (may not be necessary)
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
LATEX_COMMANDS = {'pi': r'\pi',
                  'sin': r'\sin',
                  'cos': r'\cos',
                  'tan': r'\tan',
                  'sec': r'\sec',
                  'csc': r'\csc',
                  'infty': r'\infty'}
                  






