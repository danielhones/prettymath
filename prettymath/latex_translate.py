"""
Maybe a rule-based approach is good here?
For example:

\frac{num}{denom} -> ((num)/(denom))
x_{string}        -> x_string
3abc              -> 3*a*b*c
x^{expr}          -> x**(expr)

I wonder if this is feasible to implement this way.
"""


def latex_to_python(latex):
    """
    Given a LaTeX string, return a corresponding Python expression
    """
    # How to approach this?
    # Maybe parse it from left to right, or maybe come up with an appropriate order of operations
    # such as: replace numbers, replace variables, replace latex commands, handle operators
    # like ^ and _, etc
    # Do some research and thinking on it.
    # Also, is it best to deal with latex as a string using indexes to refer to substrings, or split it
    # into a list of characters, or something else?
    pass


def parenthesize(x):
    """Return x surrounded by open and close parentheses"""
    cast = type(x)
    return cast('(') + x + cast(')')


def find_next_latex_arg(string):
    return find_next_matched_pair('{}', string)


def find_next_matched_pair(chars, string):
    """
    Given the outer characters to match in a string, returns the outermost of nested matches,
    with the characters stripped off.

    For example:
    find_next_matched_pair('()', '(2*(3+z))') returns 2*(3+z)
    """
    # TODO: Maybe this function needs to return both the matched part and the remainder of the string?
    #       How else to continue with parsing after stripping off the argument?  Maybe this whole module
    #       can work on a generator that returns the string character by character?
    left_char = chars[0]
    right_char = chars[1]
    try:
        initial_index = string.index(left_char)  # This should almost always be 0
        unmatched_chars = 1
    except ValueError:
        raise LatexTranslationError('Failed to find first occurence of', left_char, 'in', string)

    index = initial_index
    while unmatched_chars > 0:
        index += 1
        if string[index] == left_char:
            unmatched_chars += 1
        elif string[index] == right_char:
            unmatched_chars -= 1

    initial_index += 1  # So we don't include the first left_char in the return value
    final_index = index
    return string[initial_index:final_index]


class LatexTranslationError(Exception):
    pass
