from math import *
from .convex_polygon import *
P = Point2d

class Pixel:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        v = [P(x, y), P(x+1., y), P(x+1., y+1.), P(x, y+1.)]
        self.poly = ConvexPolygon(v)

    def trim_outer(self, p0, p1, reverse=False):
        assert(type(p0) == Point2d)
        assert(type(p1) == Point2d)
        tri = ConvexPolygon([P(0.0, 0.0), p0, p1])
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

    # Returns a pair of y intercepts for an x value.
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

    # Returns a pair of x intercepts for a y value.
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

    def points_on_grid(self):
        p = []
        x = 0.0
        seeking = True
        while seeking:
            y_pair = self.solve_y(x)
            if y_pair:
                p.append(Point2d(x, y_pair[0]))
                p.append(Point2d(x, y_pair[1]))
            else:
                seeking = False
            x += 1.0

        seeking = True
        x = -1.0
        while seeking:
            y_pair = self.solve_y(x)
            if y_pair:
                p.append(Point2d(x, y_pair[0]))
                p.append(Point2d(x, y_pair[1]))
            else:
                seeking = False
            x -= 1.0

        seeking = True
        y = 0.0
        while seeking:
            x_pair = self.solve_x(y)
            if x_pair:
                p.append(Point2d(x_pair[0], y))
                p.append(Point2d(x_pair[1], y))
            else:
                seeking = False
            y += 1.0

        seeking = True
        y = -1.0
        while seeking:
            x_pair = self.solve_x(y)
            if x_pair:
                p.append(Point2d(x_pair[0], y))
                p.append(Point2d(x_pair[1], y))
            else:
                seeking = False
            y -= 1.0

        return p

    def points_in_pixel(self, x, y):
        eps = 0.00001
        result = set()

        # Lower edge
        x_pair = self.solve_x(y)
        if x_pair:
            (x0, x1) = x_pair
            if abs(x0 - x1) > eps:
                if x0 >= x and x0 <= x+1:
                    result.add(P(x0, y))
                if x1 >= x and x1 <= x+1:
                    result.add(P(x1, y))
        # Right edge
        y_pair = self.solve_y(x+1.)
        if y_pair:
            (y0, y1) = y_pair
            if abs(y0 - y1) > eps:
                if y0 >= y and y0 <= y+1:
                    result.add(P(x+1., y0))
                if y1 >= y and y1 <= y+1:
                    result.add(P(x+1., y1))
        # Upper edge
        x_pair = self.solve_x(y+1.)
        if x_pair:
            (x0, x1) = x_pair
            if abs(x0 - x1) > eps:
                if x0 >= x and x0 <= x+1:
                    result.add(P(x0, y+1.))
                if x1 >= x and x1 <= x+1:
                    result.add(P(x1, y+1.))
        # Left edge
        y_pair = self.solve_y(x)
        if y_pair:
            (y0, y1) = y_pair
            if abs(y0 - y1) > eps:
                if y0 >= y and y0 <= y+1:
                    result.add(P(x, y0))
                if y1 >= y and y1 <= y+1:
                    result.add(P(x, y1))
        return result

def raster_ellipse(a, b, th, nudge):
    assert(a > 1. and b > 1.)
    min_x = None
    max_x = None
    min_y = None
    max_y = None
    eps = 0.00001
    outer = Ellipse(a, b, th, nudge)
    inner = Ellipse(a-1., b-1., th, nudge)
    
    all_points = outer.points_on_grid() + inner.points_on_grid()

    # Now create a sparse array of pixels from the lists.
    # For now I'm going to re-solve. I know it's inefficient, so
    # that will be something to optimize.
    candidates = set()
    for point in all_points:
        x = point.x
        y = point.y
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

        if (x, y) in pixels:
            continue

        p = Pixel(x, y)
        trimmed = False
        # No double points.
        points = outer.points_in_pixel(x, y)

        if (len(points) >= 2):
            # To be honest, it's a huge pain to account for
            # situtations other than a pair, and it will not 
            # likely make a huge difference.
            l = list(points)
            p.trim_outer(l[0], l[1])
            trimmed = True

        # Repeat for inner vertices.

        points = inner.points_in_pixel( x, y)
        if (len(points) >= 2):
            l = list(points)
            p.trim_inner(l[0], l[1])
            trimmed = True

        if trimmed:
            pixels[(x, y)] = p

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

