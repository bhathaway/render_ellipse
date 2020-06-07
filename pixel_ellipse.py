# I want this python script to be able to generate ascii art
# of ellipses based on command line parameters.

from math import *
from convex_polygon import *

class Pixel:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        v = [(x, y), (x+1., y), (x+1., y+1.), (x, y+1.)]
        self.poly = ConvexPolygon(v)

    def trim_outer(self, p0, p1, reverse=False):
        assert(type(p0) == tuple)
        assert(len(p0) >= 2)
        assert(type(p1) == tuple)
        assert(len(p1) >= 2)
        tri = ConvexPolygon([(0., 0.), p0, p1])
        # Ignore double solutions. We can only get away with
        # this because we're using unit thickness ellipses.
        eps = 0.00001
        a = tri.area()

        swap = False
        if abs(a) < eps:
            return
        elif reverse:
            if a > 0:
                swap = True
        else:
            if a < 0:
                swap = True

        if swap:
            temp = p1
            p1 = p0
            p0 = temp

        self.poly.trim(p0, p1)

    def trim_inner(self, p0, p1):
        self.trim_outer(p0, p1, True)

class Ellipse(object):
    def __init__(self, a, b, th, nudge=(0., 0.)):
        self.a = float(a)
        self.b = float(b)
        self.th = float(th)
        self.nudge = nudge
        c = cos(th)
        s = sin(th)
        self.A = (c*c)/(a*a) + (s*s)/(b*b)
        self.B = 2*c*s*(1.0/(a*a) - 1.0/(b*b))
        self.C = (s*s)/(a*a) + (c*c)/(b*b)

    def solve_y(self, x):
        A = self.A
        B = self.B
        C = self.C
        x0 = self.nudge[0]
        y0 = self.nudge[1]
        u = x - x0
        det = -4*A*C*u*u + B*B*u*u + 4*C
        if det >= 0:
            r = sqrt(det)
            return ((r-B*u)/(2*C)+y0, (-r-B*u)/(2*C)+y0)
        else:
            return None

    def solve_x(self, y):
        A = self.A
        B = self.B
        C = self.C
        x0 = self.nudge[0]
        y0 = self.nudge[1]
        v = y - y0
        det = -4*A*C*v*v + B*B*v*v + 4*A
        if det >= 0:
            r = sqrt(det)
            return ((r-B*v)/(2*A)+x0, (-r-B*v)/(2*A)+x0)
        else:
            return None

def ellipse(x, y, th, a, b):
    X = x * cos(th) + y * sin(th)
    Y = x * sin(th) - y * cos(th)
    return (X*X) / (a*a) + (Y*Y) / (b*b)


def ellipse_points(e):
    assert(type(e) == Ellipse)
    p = []
    x = 0.
    seeking = True
    while seeking:
        y_pair = e.solve_y(x)
        if y_pair:
            p.append((x, y_pair[0]))
            p.append((x, y_pair[1]))
        else:
            seeking = False
        x += 1.

    seeking = True
    x = -1.
    while seeking:
        y_pair = e.solve_y(x)
        if y_pair:
            p.append((x, y_pair[0]))
            p.append((x, y_pair[1]))
        else:
            seeking = False
        x -= 1.

    seeking = True
    y = 0.
    while seeking:
        x_pair = e.solve_x(y)
        if x_pair:
            p.append((x_pair[0], y))
            p.append((x_pair[1], y))
        else:
            seeking = False
        y += 1.

    seeking = True
    y = -1.
    while seeking:
        x_pair = e.solve_x(y)
        if x_pair:
            p.append((x_pair[0], y))
            p.append((x_pair[1], y))
        else:
            seeking = False
        y -= 1.

    return p

def raster_ellipse(a, b, th, nudge):
    assert(a > 1. and b > 1.)
    min_x = None
    max_x = None
    min_y = None
    max_y = None
    eps = 0.00001
    outer = Ellipse(a, b, th, nudge)
    inner = Ellipse(a-1., b-1., th, nudge)
    
    outer_points = ellipse_points(outer)
    inner_points = ellipse_points(inner)
    both = inner_points + outer_points

    # Now create a sparse array of pixels from the lists.
    # For now I'm going to re-solve. I know it's inefficient, so
    # that will be something to optimize.
    candidates = set()
    for point in both:
        (x, y) = point
        candidates.add((floor(x), floor(y)))
        if floor(x) == x:
            # Include both sides
            candidates.add((floor(x)-1, floor(y)))
        if floor(y) == y:
            candidates.add((floor(x), floor(y)-1))

    pixels = {}
    for (x, y) in candidates:
        if not min_x:
            min_x = x
            max_x = x
            min_y = y
            max_y = y
        if x > max_x:
            max_x = x
        if x < min_x:
            min_x = x
        if y > max_y:
            max_y = y
        if y < min_y:
            min_y = y

        if not (x, y) in pixels:
            p = Pixel(x, y)
            trimmed = False
            # No double points.
            points = set()
            # Lower edge
            x_pair = outer.solve_x(y)
            if x_pair:
                (x0, x1) = x_pair
                if abs(x0 - x1) > eps:
                    if x0 >= x and x0 <= x+1:
                        points.add((x0, y))
                    if x1 >= x and x1 <= x+1:
                        points.add((x1, y))
            # Right edge
            y_pair = outer.solve_y(x+1.)
            if y_pair:
                (y0, y1) = y_pair
                if abs(y0 - y1) > eps:
                    if y0 >= y and y0 <= y+1:
                        points.add((x+1., y0))
                    if y1 >= y and y1 <= y+1:
                        points.add((x+1., y1))
            # Upper edge
            x_pair = outer.solve_x(y+1.)
            if x_pair:
                (x0, x1) = x_pair
                if abs(x0 - x1) > eps:
                    if x0 >= x and x0 <= x+1:
                        points.add((x0, y+1.))
                    if x1 >= x and x1 <= x+1:
                        points.add((x1, y+1.))
            # Left edge
            y_pair = outer.solve_y(x)
            if y_pair:
                (y0, y1) = y_pair
                if abs(y0 - y1) > eps:
                    if y0 >= y and y0 <= y+1:
                        points.add((x, y0))
                    if y1 >= y and y1 <= y+1:
                        points.add((x, y1))

            if (len(points) >= 2):
                # To be honest, it's a huge pain to account for
                # situtations other than a pair, and it will not 
                # likely make a huge difference.
                l = list(points)
                p.trim_outer(l[0], l[1])
                trimmed = True

            # Repeat for inner vertices.
            points.clear()
            # Lower edge
            x_pair = inner.solve_x(y)
            if x_pair:
                (x0, x1) = x_pair
                if abs(x0 - x1) > eps:
                    if x0 >= x and x0 <= x+1:
                        points.add((x0, y))
                    if x1 >= x and x1 <= x+1:
                        points.add((x1, y))
            # Right edge
            y_pair = inner.solve_y(x+1.)
            if y_pair:
                (y0, y1) = y_pair
                if abs(y0 - y1) > eps:
                    if y0 >= y and y0 <= y+1:
                        points.add((x+1., y0))
                    if y1 >= y and y1 <= y+1:
                        points.add((x+1., y1))
            # Upper edge
            x_pair = inner.solve_x(y+1.)
            if x_pair:
                (x0, x1) = x_pair
                if abs(x0 - x1) > eps:
                    if x0 >= x and x0 <= x+1:
                        points.add((x0, y+1.))
                    if x1 >= x and x1 <= x+1:
                        points.add((x1, y+1.))
            # Left edge
            y_pair = inner.solve_y(x)
            if y_pair:
                (y0, y1) = y_pair
                if abs(y0 - y1) > eps:
                    if y0 >= y and y0 <= y+1:
                        points.add((x, y0))
                    if y1 >= y and y1 <= y+1:
                        points.add((x, y1))

            if (len(points) >= 2):
                # To be honest, it's a huge pain to account for
                # situtations other than a pair, and it will not 
                # likely make a huge difference.
                l = list(points)
                p.trim_inner(l[0], l[1])
                trimmed = True

            if trimmed:
                pixels[(x, y)] = p
        # endif
    #end for
    return [[(min_x, min_y), (max_x, max_y)], pixels]

def render_raster(raster):
    [(min_x, min_y), (max_x, max_y)] = raster[0]
    pixels = raster[1]
    s = ''
    y = max_y
    while y >= min_y:
        x = min_x
        while x <= max_x:
            if (x, y) in pixels:
                p = pixels[(x, y)]
                a = p.poly.area()
                if a < 0.25:
                    s += ' '
                elif a < 0.5:
                    s += '.'
                elif a < 0.75:
                    s += 'o'
                else:
                    s += 'O'
            else:
                s += ' '
            x+=1.0
        y -= 1.0
        s+='\n'
    return s

