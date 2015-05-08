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
    '_': (1, '', '{}'),
    'sqrt': (2, '', '[]'),
    'log': (2, '', '_{}'),
    'ln': (1, '', '{}'),
    'lg': (1, '', '{}'),
}

# These commands (including Greek letters) take no arguments, just get a backslash before
# them to turn them into LaTeX commands.
LATEX_COMMANDS_WITHOUT_ARGS = [
    'sin',
    'cos',
    'tan',
    'cot',
    'sec',
    'csc',
    'arcsin',
    'arccos',
    'arctan',
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
    'omega', 'Omega',
]

LATEX_COMMANDS_WITHOUT_ARGS.extend(greek_letters)