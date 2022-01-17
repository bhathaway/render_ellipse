# This python script will generate ascii art for a square rotated
# by a certain angle.

from math import *
from convex_polygon import *

def in_square(square, low_x, low_y):
    samples = 5
    dx = 1.0 / samples
    dx_2 = dx / 2.0

    in_count = 0
    for k in range(samples):
        y = low_y + dx_2 + k * dx
        for i in range(samples):
            x = low_x + dx_2 + i * dx
            if square.contains((x, y)):
                in_count += 1
    return 2 * in_count > samples * samples

# 'a' is the length of a side
# 'th' is the angle in radians.
# 'nudge' is a vector that offsets the square
# for a potentially better rendering.
def raster_square(a, th, nudge):
    assert(a > 1)
    assert(abs(nudge[0]) < 1. and abs(nudge[1]) < 1.)
    diag = ceil(a * sqrt(2.)/2.)
    min_x = -diag - 1
    max_x = diag + 1
    min_y = -diag - 1
    max_y = diag + 1

    x_factor = (a*sqrt(2.)/2.) * cos(th)
    y_factor = (a*sqrt(2.)/2.) * sin(th)
    coordinates = [(x_factor + nudge[0], y_factor + nudge[1]),\
                   (-y_factor + nudge[0], x_factor + nudge[1]),\
                   (-x_factor + nudge[0], -y_factor + nudge[1]),\
                   (y_factor + nudge[0], -x_factor + nudge[1])]
    square = ConvexPolygon(coordinates)
    result = ""
    for y in range(max_y - 1, min_y - 1, -1):
        for x in range(min_x, max_x, 1):
            if in_square(square, float(x), float(y)):
                result += 'Q'
            else:
                result += ' '
        result += '\n'
    return result

