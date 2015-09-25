"""
Unit tests for latex_translate
"""

import unittest
from prettymath.latex_translate import latex_to_python
from prettymath.latex_translate import parenthesize
from prettymath.latex_translate import find_next_matched_pair
from collections import deque


class TestLatexTranslate(unittest.TestCase):
    """
    def test_integer_translate(self):
        self.assertEqual(latex_to_python('3'), '3.0')
        self.assertEqual(latex_to_python('65'), '65.0')
        self.assertNotEqual(latex_to_python('65'), '6.05.0')

    def test_frac(self):
        self.assertEqual(latex_to_python('\frac{3/2}'), '((3.0)/(2.0))')

    def test_addition(self):
        self.assertEqual(latex_to_python('4+x'), '4.0+x')
        self.assertEqual(latex_to_python('35+z'), '35.0+z')
        self.assertEqual(latex_to_python('x+y+4'), 'x+y+4.0')

    def test_implicit_multiplication(self):
        self.assertEqual(latex_to_python('3xy'), '3*x*y')

    def test_subscript(self):
        self.assertEqual(latex_to_python('x_{0}', 'x_0'))
        self.assertNotEqual(latex_to_python('x_{1}', 'x_1.0'))

    def test_superscript(self):
        self.assertEqual(lwp('x^{3}'), 'x**(3.0)')
    """
    pass


class TestUtilityFunctions(unittest.TestCase):
    def test_parenthesize(self):
        self.assertEqual(parenthesize('2+x'), '(2+x)')
        self.assertEqual(parenthesize(('2', '+', 'x')), ('(', '2', '+', 'x', ')'))
        self.assertEqual(parenthesize(['2', '+', 'x']), ['(', '2', '+', 'x', ')'])
        self.assertEqual(parenthesize(deque(['2', '+', 'x'])), deque(['(', '2', '+', 'x', ')']))

    def test_find_next_matched_pair(self):
        self.assertEqual(find_next_matched_pair('{}', '{3+x}'), '3+x')
        self.assertEqual(find_next_matched_pair('()', '(x+2*(4+z))'), 'x+2*(4+z)')
        self.assertNotEqual(find_next_matched_pair('{}', '{3+x}{2}'), '3+x}{2')
