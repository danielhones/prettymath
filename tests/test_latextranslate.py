"""
Unit tests for latex_translate
"""

import unittest
from prettymath.latex_translate import latex_to_python
from prettymath.latex_translate import parenthesize
from prettymath import latex_lexer
from ply import lex
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


class TestLatexLexer(unittest.TestCase):
    def setUp(self):
        self.lexer = lex.lex(module=latex_lexer)

    def test_command(self):
        self.lexer.input('\\frac')
        token = next(self.lexer)
        self.assertEqual(token.type, 'COMMAND')
        self.assertEqual(token.value, '\\frac')

    def test_exponent(self):
        self.lexer.input('^{2}')
        token = next(self.lexer)
        self.assertEqual(token.type, 'EXPONENT')
        self.assertEqual(token.value, '^')

    def test_argument(self):
        self.lexer.input('{x+2}')
        token = next(self.lexer)
        self.assertEqual(token.type, 'ARGUMENT')
        self.assertEqual(token.value, 'x+2')

    def test_variable(self):
        self.lexer.input('x+2')
        token = next(self.lexer)
        self.assertEqual(token.type, 'VARIABLE')
        self.assertEqual(token.value, 'x')

    def test_integer(self):
        self.lexer.input('13+x')
        token = next(self.lexer)
        self.assertEqual(token.type, 'INTEGER')
        self.assertEqual(token.value, '13')

    def test_float(self):
        self.lexer.input('7.3+x')
        token = next(self.lexer)
        self.assertEqual(token.type, 'FLOAT')
        self.assertEqual(token.value, '7.3')

    def test_float_again(self):
        self.lexer.input('.25+42')
        token = next(self.lexer)
        self.assertEqual(token.type, 'FLOAT')
        self.assertEqual(token.value, '.25')


class TestUtilityFunctions(unittest.TestCase):
    def test_parenthesize(self):
        result = ['(', '2', '+', 'x', ')']
        self.assertEqual(parenthesize('2+x'), '(2+x)')
        self.assertEqual(parenthesize(['2', '+', 'x']), result)
        self.assertEqual(parenthesize(('2', '+', 'x')), tuple(result))
        self.assertEqual(parenthesize(deque(['2', '+', 'x'])), deque(result))
