"""
GUI to test the realtime update and rendering of PrettyEquation instance

add a second label to display raw_eq to insure it is equal to what latex_eq is displaying
"""


from Tkinter import *
from prettymath.prettyexpression import PrettyExpression
import matplotlib
matplotlib.use('TkAgg')
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure


root = Tk()
root.title("PrettyMath Test GUI")


def update(*args):
    f.clear()
    # ha and va are horizontal and vertical alignment, respectively:
    f.text(.5, .5, equation.latex, size='x-large', ha='center', va='center')
    canvas.show()


def add_key(event):
    equation.add_keypress(event)


def clear(*args):
    equation.reset()
    update()


f = Figure(figsize=(5, 3), dpi=100, facecolor='white')

equation = PrettyExpression()
equation.add_observer(update)

canvas = FigureCanvasTkAgg(f, master=root)
canvas.show()

canvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=1)
canvas._tkcanvas.pack(side=TOP, fill=BOTH, expand=1)

button = Button(root, text='Clear', command=clear)
button.pack(side=BOTTOM)

root.bind('<Return>', clear)
root.bind('<Key>', add_key)
root.focus()
update()

root.mainloop()
