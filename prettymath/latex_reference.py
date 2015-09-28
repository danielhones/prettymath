"""
(c) Daniel Hones 2014

MIT License
"""


# This dictionary maps LaTeX commands to the number of arguments each one takes, and a special instruction,
# and the character(s) to use to surround the first argument of the Latex command.  If three characters are given
# (like '_{}'), the first two go in front of the argument, the last one closes it.
LATEX_COMMANDS_WITH_ARGS = {
    '/': (2, 'active data', '{}'),
    'slash': (2, 'active data', '{}'),
    '^': (1, '', '{}'),
    'asciicircum': (1, '', '{}'),
    '_': (1, '', '{}'),
    'underscore': (1, '', '{}'),
    'sqrt': (2, '', '[]'),
    'log': (2, '', '_{}'),
    'ln': (1, '', '{}'),
    'lg': (1, '', '{}'),
}

# These commands (including Greek letters) take no arguments, just get a backslash before
# them to turn them into LaTeX commands, and they're called functions because they turn into
# Python math functions, so in PrettyExpression we also add parentheses around the cursor
LATEX_COMMAND_FUNCTIONS = [
    'sin',
    'cos',
    'tan',
    'cot',
    'sec',
    'csc',
    'arcsin',
    'arccos',
    'arctan',
    'sinh',
    'cosh',
    'tanh',
]


LATEX_COMMANDS_WITHOUT_ARGS = []

# Most of these are commented out for now because I've decided to limit the possible Greek letters
# to solve the epsilon/psi problem in.  Will probably add back in the more popular ones
greek_letters = [
    # 'alpha',
    # 'beta',
    # 'gamma', 'Gamma',
    # 'delta', 'Delta',
    # 'epsilon', 'varepsilon',
    # 'zeta',
    # 'eta',
    'theta', # 'vartheta', 'Theta',
    # 'iota',
    # 'kappa',
    # 'lambda', 'Lambda',
    # 'mu',
    # 'nu',
    # 'xi', 'Xi',
    'pi', 'Pi',
    # 'rho', 'varrho',
    # 'sigma', 'Sigma',
    # 'tau',
    # 'upsilon', 'Upsilon',
    # 'phi', 'varphi', 'Phi',
    # 'chi',
    # 'psi', 'Psi',
    'omega', # 'Omega',
]

LATEX_COMMANDS_WITHOUT_ARGS.extend(greek_letters)

CURSOR = '|'
