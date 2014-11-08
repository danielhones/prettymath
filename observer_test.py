from mathentry import *

a = PrettyEquation()
b = Observer()

a.add_observer(b.cb)
a.test_observe()


