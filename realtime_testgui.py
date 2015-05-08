"""
GUI to test the realtime update and rendering of PrettyEquation instance

add a second label to display raw_eq to insure it is equal to what latex_eq is displaying
"""


from Tkinter import *
import ttk
from prettymath.prettyexpression import PrettyExpression
import matplotlib
matplotlib.use('TkAgg')
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure



root = Tk()
root.title("Embedding in TK")

def update(*args):
    f.clear()
    # ha and va are horizontal and vertical alignment, respectively:
    f.text(.5, .5, equation.get_latex(), size='x-large', ha='center', va='center')
    canvas.show()

def add_key(event):
    equation.add_keypress(event)

def clear(*args):
    equation.reset()
    entry_string.set('')
    f.clear()
    canvas.show()

f = Figure(figsize=(5,3), dpi=100, facecolor='white')

entry_string = StringVar()
equation = PrettyExpression()
equation.add_observer(update)

canvas = FigureCanvasTkAgg(f, master=root)
canvas.show()

canvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=1)
entry = ttk.Entry(root, textvariable=entry_string)
canvas._tkcanvas.pack(side=TOP, fill=BOTH, expand=1)
entry.pack(side=TOP)

button = Button(root, text='Clear', command=clear)
button.pack(side=BOTTOM)

entry.bind('<Return>', clear)
entry.bind('<Key>', add_key)
entry.focus()

update()

root.mainloop()
