"""
(c) Daniel Hones 2014

MIT License
"""


import latex_reference


class DataContainer(object):
    def __init__(self, data=None):
        self._data_items = [data]
        self.active_item = self
        self.cursor_index = len(self._data_items) - 1

    @property
    def data(self):
        """Return a flattened list of _data_items contained by this object"""
        accumulated_data = []
        for i in self._data_items:
            if type(i) is str:
                accumulated_data.append(i)
            else:
                accumulated_data.extend(i.data)
        return accumulated_data

    def insert_at_cursor(self, char):
        self._data_items.insert(self.cursor_index, char)
        self.cursor_index += 1

    def new_term(self):
        """Remove cursor, place it in a new DataContainer, and return the object"""
        print "Got to new_term in DataContainer()"
        del self._data_items[self.cursor_index]
        return DataContainer(data=latex_reference.CURSOR)


class Operator(DataContainer):
    pass


class LatexCommand(DataContainer):
    def __init__(self, cmd='', args=0, first_arg_char=None):
        if cmd == '/':
            self.command = r'\frac'  # This is just a special case
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
        # Then accumulate the _data_items from the arguments:
        for arg in self.arguments:
            accumulated_data.extend( arg.get_data() )
        return accumulated_data

    def __str__(self):
        return ''.join( self.get_data() )


class Argument(DataContainer):
    def set_enclosing_chars(self, chars):
        # May not be necessary, but it could be handy to hold onto the enclosing characters separately
        # from their place in self._data_items
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
        accumulated_data.append(self.right_enclosing_chars)
        return accumulated_data
