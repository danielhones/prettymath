# !!! test-gui for math entry

from Tkinter import *
import ttk
import mathentry

"""
class entry_gui(Tk):
    def do_something(*args):
        formatted_string.set(raw_string.get())
        raw_string.set('')
        return

    def __init__(self, parent):
        Tk.__init__(self, parent)
        self.initialize()
"""        

def key(event):
    mathentry.translate_key()
    return

root = Tk()
root.title('Test GUI')

# Make variables:
entry_string = StringVar()
equation = mathentry.PrettyEquation()

# Create widgets:
content_frame = ttk.Frame(root, padding=(5, 5, 5, 0))
entry = ttk.Entry(content_frame, textvariable=entry_string, justify='center')
clear_button = ttk.Button(content_frame, text='Clear') 
pretty = ttk.Label(content_frame,
                   border=2,
                   relief='sunken',
                   anchor='nw',
                   wraplength=300)

# Set up grid:
content_frame.grid(column=0, row=0, sticky='NSEW')
entry.grid(column=0, row=0, columnspan=2, sticky='EW')
clear_button.grid(column=2, row=0, sticky='E')
pretty.grid(column=0, row=1, columnspan=3, sticky='NSEW')

root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)
content_frame.columnconfigure(0, weight=1)
content_frame.columnconfigure(1, weight=1)
content_frame.columnconfigure(2, weight=0)
content_frame.rowconfigure(1, weight=1)

entry.focus()
entry.bind('<Key>', key)

root.mainloop()
