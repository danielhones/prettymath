"""
(c) Daniel Hones 2014

MIT License


Defines constants for mathentry module
"""

import platform

# These are characters that that close the current active term and start a new one.
# These characters exist outside of the local term:
SPECIAL_CHARS = r'=+-*/(^'

# This is the list that is inserted when a new term is formed. The pipe symbol is used as a cursor
NEW_ACTIVE_TERM = ['{', '|', '}']

# When a new active term is made, this is the cursor index appended onto the cursor index stack:
NEW_TERM_INDEX = 1

# Ignore these keys (may not be necessary)
IGNORE_THESE_KEYSYMS = ['Shift_L', 'Shift_R', 'Alt_L', 'Alt_R', 'Control_L', 'Control_R']



if platform.system() == 'Darwin':
    IGNORE_THESE_KEYCODES = (131330, 131332,    # shift, but only sometimes???
                             131074, 131076,    # Shift
                             1048584,           # Super (left) or Control left
                             270336,            # Control right
                             )

