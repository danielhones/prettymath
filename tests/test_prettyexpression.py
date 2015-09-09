"""
Unit tests for PrettyExpression class
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


BACKSPACE_KEY = Key(keysym="BackSpace")
LEFT_ARROW_KEY = Key(keysym="Left")
RIGHT_ARROW_KEY = Key(keysym="Right")
UP_ARROW_KEY = Key(keysym="Up")
DOWN_ARROW_KEY = Key(keysym="Down")


class TestPrettyExpression(unittest.TestCase):
    def setUp(self):
        self.expression = PrettyExpression()
        new_keystream = make_keystream("y=x+2")
        for i in new_keystream:
            self.expression.add_keypress(i)

    def test_cursorless_latex(self):
        self.assertEqual(self.expression.cursorless_latex, "$y=x+2$")

    def test_latex(self):
        self.assertEqual(self.expression.latex, "$y=x+2|$")

    def test_reset(self):
        self.expression.reset()
        self.assertEqual(self.expression.latex, "$|$")
        self.assertEqual(self.expression.cursorless_latex, "$$")
        self.assertEqual(str(self.expression), "|")

    def test_backspace(self):
        self.expression.add_keypress(BACKSPACE_KEY)
        self.assertEqual(self.expression.latex, "$y=x+|$")

    def test_delete_char(self):
        pass

    def test_left_arrow_key(self):
        self.expression.add_keypress(LEFT_ARROW_KEY)
        self.assertEqual(self.expression.latex, "$y=x+|2$")

    def test_right_arrow_key(self):
        self.expression.add_keypress(RIGHT_ARROW_KEY)
        self.assertEqual(self.expression.latex, "$y=x+2|$")
        self.expression.add_keypress(LEFT_ARROW_KEY)
        self.expression.add_keypress(LEFT_ARROW_KEY)
        self.expression.add_keypress(RIGHT_ARROW_KEY)
        self.assertEqual(self.expression.latex, "$y=x+|2$")

    def test_up_arrow_key(self):
        pass

    def test_down_arrow_key(self):
        pass


if __name__ == '__main__':
    unittest.main()
