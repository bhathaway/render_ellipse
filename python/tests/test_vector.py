import sys
sys.path.append('..')
from convex_polygon import *

v = Vector2d(1, 2)
n1 = v.normal()
assert(n1.x == -2)
assert(n1.y == 1)

assert(v.dot(n1) == 0)

print("Passed!")

