import sys
sys.path.append('..')
from pixel_ellipse import *

p = raster_ellipse(20, 14, 0.64, (0.0, 0.5))

s = render_raster(p)
print(s)
