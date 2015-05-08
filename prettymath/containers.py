"""
(c) Daniel Hones 2014

MIT License
"""


import latex_reference

class DataContainer(object):
    def __init__(self, data=None):
        self.data = [data]
        self.active_item = self
        self.cursor_index = len(self.data) - 1
        
    def get_data(self):
        accumulated_data = []
        for i in self.data:
            if type(i) is str:
                accumulated_data.append(i)
            else:
                accumulated_data.extend( i.get_data() )
        return accumulated_data
    
    def insert_at_cursor(self, char):
        self.data.insert(self.cursor_index, char)
        self.cursor_index += 1

        
class Operator(DataContainer):
    def __init__(self):
        pass
    def get_data(self):
        # Return as a list so that functions that call this one can .extend it to a list:
        return [self.data]

    
class LatexCommand(DataContainer):
    def __init__(self, cmd='', args=0, first_arg_char=None):
        if cmd == '/':
            self.command = r'\frac' # This is just a special case
        else:
            self.command = cmd

        self.arguments = []
        self.num_arguments = len(self.arguments) # might not end up needing this
        for i in range(args):
            self.arguments.append( Argument() )
        self.arguments[0].set_enclosing_chars(first_arg_char) 

    def get_data(self):
        # This should be the LaTeX command itself, eg '\frac':
        accumulated_data = [self.command]
        # Then accumulate the data from the arguments:
        for arg in self.arguments:
            accumulated_data.extend( arg.get_data() )
        return accumulated_data

    def __str__(self):
        return ''.join( self.get_data() )


class Argument(DataContainer):
    def set_enclosing_chars(self, chars):
        # May not be necessary, but it could be handy to hold onto the enclosing characters separately
        # from their place in self.data
        if len(chars) > 2:
            self.left_enclosing_chars = chars[0:2]
        else:
            self.left_enclosing_chars = chars[0]
        self.right_enclosing_chars = chars[-1]

    def  __init__(self, enclosing_chars='{}'):
        super(Argument, self).__init__()
        self.set_enclosing_chars(enclosing_chars)

    def get_data(self):
        accumulated_data = [self.left_enclosing_chars]
        accumulated_data.extend( super(Argument, self).get_data )
        accumulated_data.append(self.right_enclosing_chars)
        return accumulated_data
