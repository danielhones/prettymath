# PrettyMath
A Python library for entry and editing of math expressions that look good

This library (will) consists of two main parts: 
- PrettyExpression, a class that takes keyboard entry as input and creates a LaTeX formatted math expression from it.
- PrettyMathWidget, a widget for use in tkinter GUI applications.

The idea of this is to handle math in a way that looks like it was written by a human.  It is much easier to read,
comprehend, and spot errors this way than in the typical way of dealing with math expressions on a computer.  Plus it
just looks a lot better and is more fun to use.

The way it works is by adding keypresses to an instance of `PrettyExpression`, which ouputs a LaTeX-formatted version to
be displayed by a matplotlib figure.  It then parses that formatted version to a Python expression, which is accessed by
the `expression` attribute of a `PrettyExpression` instance.

This project is very rough now, but has some decent functionality.  To get a feel for what it's like, run `python
calc_example.py` and play around with it.  Pressing `<Enter>` will evaluate the expression you've entered and display
the result in the lower frame.  I have plans to make a much more full-featured calculator with this library which will
include.

# Requirements
- Python 2.7
- [matplotlib](http://matplotlib.org/) (only for calc_example.py)
- [ply](http://www.dabeaz.com/ply/)

