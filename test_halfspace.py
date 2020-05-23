from convex_polygon import *

h = HalfSpace((0, 0), (1, 0))
assert(h.contains((0,0)))
assert(h.contains((0, 1)))
assert(not h.contains((0, -1)))

x = h.intersection((0, -1), (1, 1))
assert(x == (0.5, 0.0))

print("Passed!")
