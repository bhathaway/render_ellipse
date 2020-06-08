import sys
sys.path.append('..')
from pixel_ellipse import *

p = Pixel(0., 0.)
p.trim_outer((1.0, 0.5), (0.5, 1.0))
p.trim_inner((0.0, 0.5), (0.5, 0.0))
assert(p.poly.area() == 0.75)

# Try reversing the vertices.
q = Pixel(0., 0.)
q.trim_outer((0.5, 1.0), (1.0, 0.5))
q.trim_inner((0.5, 0.0), (0.0, 0.5))
assert(q.poly.area() == 0.75)

print("Passed!")
