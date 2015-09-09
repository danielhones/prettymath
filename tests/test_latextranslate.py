"""
Unit tests for latex_translate
"""

from prettymath.latex_translate import latex_to_python as l2p
from prettymath.latex_translate import parenthesize
from prettymath.latex_translate import find_next_matched_pair as fnmp
import unittest


class TestLatexTranslate(unittest.TestCase):
    """
    def test_integer_translate(self):
        self.assertEqual(l2p('3'), '3.0')
        self.assertEqual(l2p('65'), '65.0')
        self.assertNotEqual(l2p('65'), '6.05.0')

    def test_frac(self):
        self.assertEqual(l2p('\frac{3/2}'), '(3.0/2.0)')

    def test_addition(self):
        self.assertEqual(l2p('4+x'), '4.0+x')
        self.assertEqual(l2p('35+z'), '35.0+z')
        self.assertEqual(l2p('x+y+4'), 'x+y+4.0')

    def test_implicit_multiplication(self):
        self.assertEqual(l2p('3xy'), '3*x*y')
    """
    pass


class TestUtilityFunctions(unittest.TestCase):
    def test_parenthesize(self):
        self.assertEqual(parenthesize('2+x'), '(2+x)')
        self.assertEqual(parenthesize(('2', '+', 'x')), ('(', '2', '+', 'x', ')'))
        self.assertEqual(parenthesize(['2', '+', 'x']), ['(', '2', '+', 'x', ')'])

    def test_find_next_matched_pair(self):
        self.assertEqual(fnmp('{}', '{3+x}'), '3+x')
        self.assertEqual(fnmp('()', '(x+2*(4+z))'), 'x+2*(4+z)')
        self.assertNotEqual(fnmp('{}', '{3+x}{2}'), '3+x}{2')
