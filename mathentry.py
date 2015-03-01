"""
(c) Daniel Hones 2014

MIT License


This file defines the PrettyMath class and MathEntryWidget class, along with some other utility 
functions and classes.

The PrettyMath class uses a tree data structure to store the LaTeX formatted math.  The tree uses
left child, right sibling representation.  Each node links to its parent, its left sibling, and its
right sibling.  'self' in the PrettyMath class definition always refers to the root of the tree, and 
the node that is currently being edited (contains the cursor) is self.active_node.  Therefore, no reference
to the root of the tree is necessary.


TODO:
* Write unit tests
* Reconfigure it so that terms that are at the same level of 'nestedness' are on the same level of the tree.
  For example, a + or - or = should create a new node in the tree that is a right sibling of the current node,
  rather than a child as is the case now.
* Some stuff is really weird and broken now (ie, typing +, -, cos, sin). Fix it
* Start thinking about how to translate the tree into a valid Python expression
* Write a few methods to help visualize the tree structure
* Figure out where error handling is needed and write it (maybe ensure that data is always a list of strings?).
* Implement delete_node or whatever needs to be done to remove a node in the tree.  Also determine
  what that even means.  Maybe a delete_subtree is also necessary.  Think about it.
"""

# These may no longer be necessary:
#from translate_functions import *  
# The only thing we use from constants now is LATEX_COMMANDS, so there is probably a neater
# way to do it.
from constants import *
import keybindings
from pprint import pprint

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
                 parent=None,
                 left_child=None,
                 left_sibling=None,
                 right_sibling=None,
                 root=None):
        self.data = data
        self.parent = parent
        self.left_child = left_child
        self.right_sibling = right_sibling
        self.left_sibling = left_sibling
        if root == None:
            self.root = self
        else:
            self.root = root

    def insert_child(self, new_data):
        if self.left_child == None:
            self.left_child = SiblingTree(new_data, root=self.root)
        else:
            new_tree = SiblingTree(new_data,
                                   left_child=self.left_child,
                                   root=self.root)
            self.left_child.parent = new_tree
            self.left_child = new_tree
        return self.left_child

    # maybe this class definition should have an insert_left_sibling method for the sake of completeness,
    # even though it won't be used by the PrettyMath class 
    def insert_right_sibling(self, new_data):
        if self.right_sibling == None:
            self.right_sibling = SiblingTree(new_data,
                                             left_sibling=self,
                                             parent=self.parent,
                                             root=self.root)
        else:
            new_tree = SiblingTree(new_data,
                                   right_sibling=self.right_sibling,
                                   left_sibling=self,
                                   parent=self.parent,
                                   root=self.root)
            self.right_sibling.left_sibling = new_tree
            self.right_sibling = new_tree
        return self.right_sibling

    # TODO: implement these methods:
    def delete_node(self):
        return

    def delete_leftchild(self):
        return

    def delete_rightsibling(self):
        return

    def delete_subtree(self):
        return
    
    def walk_tree(self):
        # Walk left_child's until there are no more, extending the list along the way,
        # then walk right siblings, then parent's right siblings

        # It is VERY important here to make result a COPY of self.data, rather than a reference to
        # it.  Otherwise, the list self.data gets mutated by this method.
        result = self.data[:]   # copy, not reference
        if self.left_child != None:
            result.extend(self.left_child.walk_tree())
        elif self.right_sibling != None:
            result.extend(self.right_sibling.walk_tree())
        elif self.parent == None:
            return result
        elif self.parent.right_sibling != None:
            result.extend(self.parent.right_sibling.walk_tree())
        return result

    def print_tree(self, indent=''):
        # How much each level is indented:
        spaces = '   '
        print indent + str(self)
        if self.left_child != None:
            self.left_child.print_tree(indent=indent+spaces)
        elif self.right_sibling != None:
            self.right_sibling.print_tree(indent=indent)
        elif self.parent == None:
            return
        elif self.parent.right_sibling != None:
            # Since we move up a level, we remove a set of spaces from indent.  Since we can't use 
            # indent - spaces, we just pass indent with one less 'spaces' indexed:
            self.parent.right_sibling.print_tree(indent=indent[len(spaces):])
        else:
            return

    def __str__(self):
        return ''.join(self.data)


class PrettyMath(Observable, SiblingTree):
    """
    This class has two main attributes: raw, which is a valid Python math expression, and latex
    which is that expression formatted to look nice in Latex.
    """
    CURSOR = r'|'

    def __init__(self, data=[CURSOR], root=None):
        # Not sure yet how to handle init since PrettyMath inherits from two classes.
        # Need to do a little more research, but for now this works.  It might even be best:
        Observable.__init__(self)
        SiblingTree.__init__(self, data=data, root=root)
        
        # Put cursor at end of data list
        # Eventually, the MathEntry widget will draw the cursor on the canvas.  But for now,
        # we do it really ghetto:
        # TODO:  Make sure this works right in all cases, especially when starting a new subtree.
        # I think it will work, but need to spend some time thinking about it.
        self.cursor_index = len(self.data) - 1
        # active_node keeps track of which node in the tree is currently being edited/actually contains the cursor
        self.active_node = self
        self.running_list = []

    def insert_child(self, new_data):
        if self.left_child == None:
            self.left_child = PrettyMath(new_data, root=self.root)
        else:
            new_tree = PrettyMath(new_data,
                                   left_child=self.left_child,
                                   root=self.root)
            self.left_child.parent = new_tree
            self.left_child = new_tree
        return self.left_child

    # maybe this class definition should have an insert_left_sibling method for the sake of completeness,
    # even though it won't be used by the PrettyMath class 
    def insert_right_sibling(self, new_data):
        if self.right_sibling == None:
            self.right_sibling = PrettyMath(new_data,
                                            left_sibling=self,
                                            parent=self.parent,
                                            root=self.root)
        else:
            new_tree = PrettyMath(new_data,
                                  right_sibling=self.right_sibling,
                                  left_sibling=self,
                                  parent=self.parent,
                                  root=self.root)
            self.right_sibling.left_sibling = new_tree
            self.right_sibling = new_tree
        return self.right_sibling

        
    def __str__(self):
        return ''.join(self.data)

    def reset(self):
        # TODO: make this work
        pass
      
    def get_latex(self):
        # Just put '$'s around the string so that matplotlib prints it as LaTeX math
        return '$' + ''.join(self.walk_tree()) + '$'

    def add_keypress(self, newkey):
        # newkey.state is a bitfield that represents modifier keys pressed simultaneously with
        # the keysym.  It is 0 if there are no modifier keys:
        func = keybindings.get_function_for(newkey.keysym, newkey.char, newkey.state)

        if func == None:
            return
        else:
            func(self.active_node, newkey)

        #if newkey.char in SPECIAL_CHARS:
            # start a new subtree for a new term:
        # This is just a simplistic way to do it for testing porpoises
        """
        if newkey.char in '+-*/=':
        """        
        # If there's nothing special that needs to be done with the new keypress, these next few lines
        # just insert the character where the cursor is and move the cursor to the right by one:
        # I wonder if there's a cleaner way to do this:
        # Can delete very soon:
        #self.active_node.data.insert(self.active_node.cursor_index, newkey.char)
        #self.active_node.cursor_index += 1


        # Check to see if the end part of running_list is something meaningful in LaTeX:
        command = self.check_for_latex_command(''.join(self.active_node.running_list))
        if command:
            size = len(command)
            # Remove all the individual letters that spell the command
            del self.active_node.data[ self.cursor_index - size : self.cursor_index ]
            
            # Replace them with a single string element containing the LaTeX command
            self.active_node.data.insert(self.cursor_index - size, LATEX_COMMANDS[command])

            # Reset running_list if it just inserted a function, otherwise make running_list
            # hold the current term.
            if command in FUNCTIONS:
                self.running_list = []
            else:
                del self.running_list[-size:]
                self.running_list.append(LATEX_COMMANDS[command])

            # Make the cursor_index right:
            self.cursor_index += 1
            
        # It's handy to have cursor_index accessible from both the root and the active_node 
        self.active_node.cursor_index = self.cursor_index
        # This should be the last thing we do:
        self.notify_observers()
        self.print_tree()
        print


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
        
