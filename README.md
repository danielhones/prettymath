# prettymath
A Python library for entry and editing of math expressions that look good

This library consists of two main parts: 
- PrettyExpression, a class that takes keyboard entry as input and creates a LaTeX formatted math expression from it.
- PrettyMathWidget, a widget for use in tkinter GUI applications.

The idea of this is to handle math in a way that looks like it was written by a human.  It is much easier to read, comprehend, and spot errors this way than in the typical way of dealing with math expressions on a computer.  Plus it just looks a lot better and is more fun to use.

This project is currently VERY unfinished, since I only get to work on it in my spare time which is scarcer than I'd like.  But you can get a very rough idea for what it will be like.  Run `python realtime_testgui.py` and type in some simple expressions.  As of now, it doesn't handle any special LaTeX formatting like superscripts or fractions, but basic entry of terms will work.
