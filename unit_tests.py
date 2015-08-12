"""
Unit tests for prettymath module
"""

from prettymath.prettyexpression import PrettyExpression
from prettymath.bindings import SHIFT, ON_NUMPAD
import unittest


class Key(object):
    def __init__(self, keysym=None, char=None, state=0):
        self.keysym = keysym
        if char is None and keysym is not None:
            self.char = self.keysym
        else:
            self.char = char
        self.state = state


def make_keystream(chars):
    return [Key(i) for i in chars]


class TestPrettyMathFunctions(unittest.TestCase):
    def setUp(self):
        pass


class TestLatexCommandInsertion(unittest.TestCase):
    def test_single_replacement(self):
        test_object = PrettyExpression()
        for keypress in make_keystream('sigma'):
            test_object.add_keypress(keypress)
        self.assertEqual(test_object.latex, r'${\sigma}|$')

    def test_multiple_replacements(self):
        test_object = PrettyExpression()
        for keypress in make_keystream('sigmapipsi'):
            test_object.add_keypress(keypress)
        self.assertEqual(test_object.latex, r'${\sigma}{\pi}{\psi}|$')

    def test_superscript(self):
        pass


class TestKeybindingFunctions(unittest.TestCase):
    def test_frac(self):
        pass

    def test_plus(self):
        test_object = PrettyExpression()
        for keypress in [Key('x'), Key('plus', '+', SHIFT), Key('3')]:
            test_object.add_keypress(keypress)
        self.assertEqual(test_object.latex, r'$x+3|$')

    def test_minus(self):
        test_object = PrettyExpression()
        for keypress in [Key('x'), Key('minus', '-'), Key('3')]:
            test_object.add_keypress(keypress)
        self.assertEqual(test_object.latex, r'$x-3|$')

    def test_equals(self):
        test_object = PrettyExpression()
        for keypress in [Key('x'),
                         Key('equal', '='),
                         Key('3')]:
            test_object.add_keypress(keypress)
        self.assertEqual(test_object.latex, r'$x=3|$')

    def test_plus_minus_and_equals(self):
        test_object = PrettyExpression()
        for keypress in [Key('x'),
                         Key('plus', '+', SHIFT),
                         Key('3'),
                         Key('equal', '='),
                         Key('y'),
                         Key('minus', '-'),
                         Key('2')]:
            test_object.add_keypress(keypress)
        self.assertEqual(test_object.latex, r'$x+3=y-2|$')


if __name__ == '__main__':
    unittest.main()
