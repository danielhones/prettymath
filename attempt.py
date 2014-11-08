#!/usr/bin/env python
import matplotlib
matplotlib.use('TkAgg')

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure
import Tkinter as Tk
import ttk


def destroy(e): sys.exit()

def change_eq(eq):
    f.clear()
    f.text(.3,.3,'$'+eq.get()+'$')
    eq.set('')
    canvas.show()
    

root = Tk.Tk()
root.title("Embedding in TK")

f = Figure(figsize=(2,1), dpi=100)

entry_string = Tk.StringVar()

canvas = FigureCanvasTkAgg(f, master=root)
canvas.show()

canvas.get_tk_widget().pack(side=Tk.TOP, fill=Tk.BOTH, expand=1)
entry = ttk.Entry(root, textvariable=entry_string)
canvas._tkcanvas.pack(side=Tk.TOP, fill=Tk.BOTH, expand=1)
entry.pack(side=Tk.TOP)
button = Tk.Button(root, text='Enter', command=lambda: change_eq(entry_string))
button.pack(side=Tk.BOTTOM)
root.bind('<Return>', change_eq(entry_string))

root.mainloop()
