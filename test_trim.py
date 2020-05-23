from pixel_ellipse import *

p = Pixel(0., 0.)
p.trim_outer((1.0, 0.5), (0.5, 1.0))
p.trim_inner((0.0, 0.5), (0.5, 0.0))
assert(p.poly.area() == 0.75)

print("Passed!")
