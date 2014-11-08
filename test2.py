# !!! test-gui for math entry

from Tkinter import *
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
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

fig = Figure()
canvas = FigureCanvasTkAgg(fig, master=root)

def update(eq):
    new_eq = '$'+eq.get()+'$'
    fig.clear()
    fig.text(0.3,0.3,new_eq)
    canvas.show()
    eq.set('')
    
clear_button = ttk.Button(content_frame, text='Clear', command=update(entry_string)) 

# Set up grid:
content_frame.grid(column=0, row=0, sticky='NSEW')
entry.grid(column=0, row=0, columnspan=2, sticky='EW')
clear_button.grid(column=2, row=0, sticky='E')
canvas.show()
canvas.get_tk_widget().grid(column=0, row=1, columnspan=3, sticky='NSEW')


root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)
content_frame.columnconfigure(0, weight=1)
content_frame.columnconfigure(1, weight=1)
content_frame.columnconfigure(2, weight=0)
content_frame.rowconfigure(1, weight=1)

entry.focus()
root.bind('<Return>', update(entry_string))

root.mainloop()

