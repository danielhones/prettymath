from Tkinter import *
import ttk

# Remember, widget.configure() will print a list of all options for
# a particular widget

root = Tk()
root.title('Test GUI')

def do_something(*args):
    formatted_string.set(raw_string.get())
    raw_string.set('')
    return

def parse(*args):
    return

formatted_string = StringVar()
raw_string = StringVar()
raw_string.set('Type something in me')
formatted_string.set('Hello')

content_frame = ttk.Frame(root, padding=5)
entry = ttk.Entry(content_frame, textvariable=raw_string)
button = ttk.Button(content_frame, text='Clicky', command=do_something, padding=3)
pretty = ttk.Label(content_frame, textvariable=formatted_string, border=2, relief='sunken', anchor='nw')

content_frame.grid(column=0, row=0, sticky='NSEW')
entry.grid(column=0, row=0, columnspan=2, sticky='EW')
pretty.grid(column=0, row=1, columnspan=3, rowspan=1, sticky='NSEW')
button.grid(column=2, row=0, sticky='E')

root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)
content_frame.columnconfigure(0, weight=1)
content_frame.columnconfigure(1, weight=1)
content_frame.columnconfigure(2, weight=0)
content_frame.rowconfigure(1, weight=1)

entry.focus()
root.bind('<Return>', do_something)

root.mainloop()
