# I want this python script to be able to generate ascii art
# of ellipses based on command line parameters.

from math import *


class Pixel:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    # Add an entry point for a line segment in counter clockwise reckoning.
    def add_cc_entry(self, x, y):
        assert(x >= self.x)
        assert(y >= self.y)
        assert(x == self.x or x == self.x + 1 or y == self.y or y == self.y + 1)
        self.cc_entry_x = x
        self.cc_entry_y = y

    def add_cc_exit(self, x, y):
        assert(x >= self.x)
        assert(x >= self.y)
        assert(x == self.x or x == self.x + 1 or y == self.y or y == self.y + 1)
        self.cc_exit_x = x
        self.cc_exit_y = y

    def get_area(self):
        pass

class Ellipse:
    def __init__(self, a, b, th):
        self.a = float(a)
        self.b = float(b)
        self.th = float(th)
        c = cos(th)
        s = sin(th)
        self.A = (c*c)/(a*a) + (s*s)/(b*b)
        self.B = 2*c*s*(1.0/(a*a) - 1.0/(b*b))
        self.C = (s*s)/(a*a) + (c*c)/(b*b)

    def solve_y(self, x):
        A = self.A
        B = self.B
        C = self.C
        det = -4*A*C*x*x + B*B*x*x + 4*C
        if det >= 0:
            r = sqrt(det)
            return ((r-B*x)/(2*C), (-r-B*x)/(2*C))
        else:
            return None

    def solve_x(self, y):
        A = self.A
        B = self.B
        C = self.C
        det = -4*A*C*y*y + B*B*y*y + 4*A
        if det >= 0:
            r = sqrt(det)
            return ((r-B*y)/(2*A), (-r-B*y)/(2*A))
        else:
            return None

def ellipse(x, y, th, a, b):
    X = x * cos(th) + y * sin(th)
    Y = x * sin(th) - y * cos(th)
    return (X*X) / (a*a) + (Y*Y) / (b*b)


