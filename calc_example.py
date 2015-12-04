"""
GUI to test the realtime update and rendering of PrettyEquation instance.

This is very sloppy, please excuse me for that.
"""


from Tkinter import *
from prettymath.prettyexpression import PrettyExpression
import matplotlib
matplotlib.use('TkAgg')
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import math


root = Tk()
root.title("PrettyMath Test GUI")


def update(*args):
    f.clear()
    # ha and va are horizontal and vertical alignment, respectively:
    f.text(.5, .5, equation.latex, size='x-large', ha='center', va='center')
    canvas.show()


def evaluate(*args):
    f2.clear()
    raw = equation.expression
    answer = eval(raw)
    if int(answer) == answer:
        answer = int(answer)
    answer = '$' + str(answer) + '$'
    f2.text(.5, .5, answer, size='x-large', ha='center', va='center')
    answer_canvas.show()


def add_key(event):
    equation.add_keypress(event)


def clear(*args):
    equation.reset()
    f2.clear()
    answer_canvas.show()
    update()


f = Figure(figsize=(4, 1), dpi=100, facecolor='white')

equation = PrettyExpression()
equation.add_observer(update)

canvas = FigureCanvasTkAgg(f, master=root)
canvas.show()
canvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=1)
canvas._tkcanvas.pack(side=TOP, fill=BOTH, expand=1)

f2 = Figure(figsize=(4, 1), dpi=100, facecolor='white')
answer_canvas = FigureCanvasTkAgg(f2, master=root)
answer_canvas.show()
answer_canvas.get_tk_widget().pack(side=BOTTOM, fill=BOTH, expand=1)
answer_canvas._tkcanvas.pack(side=BOTTOM, fill=BOTH, expand=1)


root.bind('<Escape>', clear)
root.bind('<Return>', evaluate)
root.bind('<Key>', add_key)
root.focus()
update()

root.mainloop()
