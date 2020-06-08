import sys
sys.path.append('..')
from convex_polygon import *
from math import *

l = [(-4, 3), (2, 5), (5, 1)]

c = ConvexPolygon(l)
assert(c.area() == -15)

l = [(-4, 3), (5, 1), (2, 5)]
c = ConvexPolygon(l)
assert(c.edge_count() == 3)
assert(c.get_vertex(0) == (-4, 3))
assert(c.get_vertex(1) == (5, 1))
assert(c.get_vertex(2) == (2, 5))
assert(c.area() == 15)

# Let's test a "Pixel"
l = [(0, 0), (1, 0), (1, 1), (0, 1)]
s = ConvexPolygon(l)
assert(s.area() == 1.0)

# How about a hexagon?
s_3 = sqrt(3.0)
l = [(0, 0), (1, 0), (1.5, s_3/2.0), (1, s_3), (0, s_3), (-0.5, s_3/2.0)]
h = ConvexPolygon(l)
assert(abs(h.area() - 1.5*s_3) < 0.000001)
print("Passed!")
