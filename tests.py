"""
Unit tests for mathentry module
"""

import prettymath
import unittest

class Key(object):
    def __init__(self, keysym, state=0):
        self.keysym = keysym
        self.state = state

def make_key_stream(keypresses):
    """
    The argument keypresses here is a string that represents a list of key presses.  This function
    makes key objects out of them (having a keysym and state) so that they can be sent as a stream for testing.
    
    Need to figure out here a way to represent arrow keys and delete and backspace.
    """
    special_keysyms = {
        '+': 'plus',
        '-': 'minus',
        '=': 'equals'
    }

    key_stream = []
    for k in keypresses:
        new_key = Key()
        if k in special_keysyms:
            new_key.keysym = special_keysyms[k]
        else:
            new_key.keysym = k
        new_key.state = 0
        key_stream.append(new_key)
    return key_stream
    
class TestPrettyMathFunctions(unittest.TestCase):
    def setUp(self):
        pass

    def test_frac(self):
        """
        To test, we need to send the stream of keypresses to a PrettyExpression object, and check that
        PrettyExpression.get_latex() returns both the proper LaTeX formatted string and the proper
        Python expression equal to the LaTeX string
        """
        ks1 = 
        ks2 = 
        test_object = PrettyExpression()

        for keypress in make_key_stream('y=3/2'):
            test_object.add_keypress(keypress)
        self.assertEqual( test_object.get_latex(), r'y=\frac{3}{2}' )

        test_object.reset()
        self.assertEqual( test_object.get_latex(), '')
        
        for keypress in make_key_stream('sin3/2pi'):
            test_object.add_keypress(keypress)
        self.assertEqual( test_object.get_latex(), r'\frac{\sin3}{2\pi}' )

        
if __name__ == '__main__':
    unittest.main()
