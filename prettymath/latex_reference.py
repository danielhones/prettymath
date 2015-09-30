"""
(c) Daniel Hones 2014

MIT License
"""


DEFAULT_DELIMITERS = ('{', '}')
PAREN_DELIMITERS = ('(', ')')
NO_DELIMITERS = ()


"""
This dictionary maps LaTeX commands to the delimiters that separate their arguments.  The value for each key is a tuple
"""
LATEX_COMMANDS_WITH_ARGS = {
    '^': DEFAULT_DELIMITERS,
    '_': DEFAULT_DELIMITERS,
    'ln': DEFAULT_DELIMITERS,
    'lg': DEFAULT_DELIMITERS,
    'sqrt': DEFAULT_DELIMITERS,
    'log': ('_{', '}{', '}'),
    'sin': PAREN_DELIMITERS,
    'cos': PAREN_DELIMITERS,
    'tan': PAREN_DELIMITERS,
    'cot': PAREN_DELIMITERS,
    'sec': PAREN_DELIMITERS,
    'csc': PAREN_DELIMITERS,
    'arcsin': PAREN_DELIMITERS,
    'arccos': PAREN_DELIMITERS,
    'arctan': PAREN_DELIMITERS,
    'sinh': PAREN_DELIMITERS,
    'cosh': PAREN_DELIMITERS,
    'tanh': PAREN_DELIMITERS,
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
    'pi', # 'Pi',
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
