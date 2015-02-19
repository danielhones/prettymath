"""
(c) Daniel Hones 2014

MIT License


This file defines the PrettyMath class and MathEntryWidget class, along with some other utility 
functions and classes.

The PrettyMath class uses a tree data structure to store the LaTeX formatted math.  The tree uses
left child, right sibling representation.  Each node links to its parent, its left sibling, its
right sibling, and the root of the tree. If a tree's root is itself, then it is the root of the 
entire tree.  A reference to the root is necessary for the walk_tree method to 

TODO:
* Implement walk_tree function.  Should this be a method in the class, or an external function?
* Implement delete_tree or whatever needs to be done to remove a node in the tree.  Also determine
  what that even means
* Set up certain characters that need to create a new term, and thus subtree (like +, *, /, etc) 
"""

# These may no longer be necessary:
from translate_functions import *
from constants import *



class Observable(object):
    def __init__(self):
        self.observers = []
    def add_observer(self, callback):
        """
        An observer here is just a callback function to call when the variable changes 
        """
        self.observers.append(callback)
    def notify_observers(self):
        for callback in self.observers:
            callback(self)

class SiblingTree(object):
    """
    A tree structure where each node can have an arbitrary number of children, using
    a left child, right sibling representation
    """
    def __init__(self,
                 data=None,
                 root=None,
                 parent=None,
                 left_child=None,
                 left_sibling=None,
                 right_sibling=None):
        self.data = data
        self.parent = parent
        self.root = root
        self.left_child = left_child
        self.right_sibling = right_sibling
        self.left_sibling = left_sibling
    def insert_child(self, new_data):
        if self.left_child == None:
            self.left_child = SiblingTree(new_data)
        else:
            new_tree = SiblingTree(new_data,
                                   left_child=self.left_child)
            self.left_child.parent = new_tree
            self.left_child = new_tree
    # maybe this class definition should have an insert_left_sibling method for the sake of completeness,
    # even though it won't be used by the PrettyMath class 
    def insert_right_sibling(self, new_data):
        if self.right_sibling == None:
            self.right_sibling = SiblingTree(new_data,
                                             left_sibling=self,
                                             parent=self.parent)
        else:
            new_tree = SiblingTree(new_data,
                                   right_sibling=self.right_sibling,
                                   left_sibling=self,
                                   parent=self.parent)
            self.right_sibling.left_sibling = new_tree
            self.right_sibling = new_tree
            

class PrettyMath(Observable, SiblingTree):
    """
    This class has two main attributes: raw, which is a valid Python math expression, and latex
    which is that expression formatted to look nice in Latex.
    """
    def __init__(self, data=[CURSOR], root=None):
        # Not sure yet how to handle init since PrettyMath inherits from two classes.
        # Need to do a little more research, but for now this works.  It might even be best:
        Observable.__init__(self)
        # It's important to explicitly pass root=self.root as an argument when creating a subtree
        if root == None:
            # If not specified, this is a new tree and the root is itself.  Basically makes the argument list
            # for __init__: root=self.root but avoids the problem of self not being defined yet
            root = self
        SiblingTree.__init__(self, data=data, root=root)
        
        # Put cursor at end of data list
        # Eventually, the MathEntry widget will draw the cursor on the canvas.  But for now,
        # we do it really ghetto:
        # TODO:  Make sure this works right in all cases, especially when starting a new subtree.
        # I think it will work, but need to spend some time thinking about it.
        self.root.cursor_in_tree = self
        self.cursor_index = len(self.data) - 1
        
        # Eventually, these will probably be implemented differently:
        self.TRANSLATE_KEYCODE = {RIGHT : move_cursor,
                                  LEFT  : move_cursor,
                                  UP    : cursor_up,
                                  DOWN  : cursor_down }
        self.TRANSLATE_CHAR = {'/'      : insert_frac,
                               '('      : open_parens,
                               ')'      : close_parens,
                               '^'      : insert_superscript,
                               '_'      : insert_subscript,
                               r'\\'    : backslash}
        
    def __str__(self):
        return ''.join(self.data)

    def get_latex(self):
        # Just put '$'s around the string so that matplotlib prints it as LaTeX math
        # eventually will return something like '$' + str(self.root.walk_tree()) + '$' or
        # whatever it needs to be
        return '$' + str(self) + '$'

    def walk_tree(self):
        # Walk left_child's until there are no more, extending the list along the way,
        # then right siblings, then parent's right siblings
        result = self.data
        if self.left_child != None:
            result.extend(self.left_child.walk_tree())
        elif self.right_sibling != None:
            result.extend(self.right_sibling.walk_tree())
        elif self.parent.right_sibling != None:
            result.extend(self.parent.right_sibling.walk_tree())
        else:
            return
        
    
    def add_keypress(self, newkey):
        if newkey.keycode in self.TRANSLATE_KEYCODE:
            self.TRANSLATE_KEYCODE[newkey.keycode](self, newkey.keycode)
            self.notify_observers()
            return

        # Ignore certain special keys for now, until they're implemented:
        if newkey.keysym in IGNORE_THESE_KEYSYMS:
            return
        if newkey.keycode in IGNORE_THESE_KEYCODES:
            return

        # This won't always be an empty block:
        if newkey.keycode in SPECIAL_KEYCODES:
            return

        if newkey.char in self.TRANSLATE_CHAR:
            # Call the function needed to do some Latex formatting
            self.TRANSLATE_CHAR[newkey.char](self)
            self.notify_observers()
            return

        #if newkey.char in SPECIAL_CHARS:
            # start a new subtree for a new term:
            
                
        # If there's nothing special that needs to be done with the new keypress, these next few lines
        # just insert the character where the cursor is and move the cursor to the right by one:
        self.data.insert(self.cursor_index, newkey.char)
        self.cursor_index += 1


        # Check to see if the end part of running_list is something meaningful in LaTeX:
        command = self.check_for_latex_command(str(self))
        if command:
            size = len(command)
            # Remove all the individual letters that spell the command
            #del self.data[ self.cursor_index[-1] - size : self.cursor_index[-1] ]
            
            # Replace them with a single string element containing the LaTeX command
            #self.data.insert(self.cursor_index - size, LATEX_COMMANDS[command])

            # Reset running_list if it just inserted a function, otherwise make running_list
            # hold the current term.
            if command in FUNCTIONS:
                self.running_list = []
            else:
                del self.running_list[-size:]
                self.running_list.append(LATEX_COMMANDS[command])
            self.latex_index[-1] -= size - 1

        # This should be the last thing we do:
        self.notify_observers()


    def check_for_latex_command(self, string):
        """
        This function checks the string to see if it contains a LaTeX command.  It checks starting
        with the last two characters and stretches towards the beginning of the string one character
        at a time.
        At the moment it uses a simple approach, which seems to work fast enough. 
        """
        for i in range(2, len(string)+1):
            if string[-i:] in LATEX_COMMANDS:
                return string[-i:]
        return None
        
