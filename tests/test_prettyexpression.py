"""
Unit tests for PrettyExpression class
"""

from prettymath.prettyexpression import PrettyExpression
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
        new_keystream = make_keystream("y=x+20")
        for i in new_keystream:
            self.expression.add_keypress(i)

    def test_latex(self):
        self.assertEqual(self.expression.latex, "$y=x+20|$")

    def test_reset(self):
        self.expression.reset()
        self.assertEqual(self.expression.latex, "$|$")
        self.assertEqual(str(self.expression), "|")

    def test_backspace(self):
        self.expression.add_keypress(BACKSPACE_KEY)
        self.assertEqual(self.expression.latex, "$y=x+2|$")

    def test_delete_char(self):
        pass

    def test_left_arrow_key(self):
        self.expression.add_keypress(LEFT_ARROW_KEY)
        self.assertEqual(self.expression.latex, "$y=x+2|0$")

    def test_right_arrow_key(self):
        self.expression.add_keypress(RIGHT_ARROW_KEY)
        self.assertEqual(self.expression.latex, "$y=x+20|$")
        self.expression.add_keypress(LEFT_ARROW_KEY)
        self.expression.add_keypress(LEFT_ARROW_KEY)
        self.expression.add_keypress(RIGHT_ARROW_KEY)
        self.assertEqual(self.expression.latex, "$y=x+2|0$")

    def test_check_for_latex_command(self):
        expr = PrettyExpression()
        for i in make_keystream("sinx"):
            expr.add_keypress(i)
        self.assertEqual(expr.latex, r"$\sin (x|)$")
        """
        expr.reset()
        for i in make_keystream("sinhx"):
            expr.add_keypress(i)
        self.assertEqual(expr.latex, r"$\sinh x|$")

        expr.reset()
        for i in make_keystream("epsilon"):
            expr.add_keypress(i)
        self.assertEqual(expr.latex, r"$\epsilon |$")
        """

    def test_up_arrow_key(self):
        pass

    def test_down_arrow_key(self):
        pass


if __name__ == '__main__':
    unittest.main()
