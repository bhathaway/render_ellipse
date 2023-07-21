import math
from ascii_shapes.pixel_ellipse import *
from ascii_shapes.convex_polygon import Vector2d

import argparse as ap
parser = ap.ArgumentParser(description='Make ASCII art ellipse')
parser.add_argument('-X', '--horizontal_radius', type=float, required=True,
    help='distance from center to horizontal edge')
parser.add_argument('-Y', '--vertical_radius', type=float, required=True,
    help='distance from center to vertical edge')
parser.add_argument('-A', '--angle', type=float, default=0.0,
    help='Angle to rotate clockwise in degrees')
parser.add_argument('-x', '--nudgex', type=float, default=0.0,
    help='x translation applied after rotation')
parser.add_argument('-y', '--nudgey', type=float, default=0.0,
    help='y translation applied after rotation')
parser.add_argument('--test', action='store_true')

args = parser.parse_args()
angle = args.angle * math.pi / 180.0

if (not args.test):
    r = raster_ellipse(args.horizontal_radius, args.vertical_radius,
        angle, Vector2d(args.nudgex, args.nudgey))
    print(render_raster(r))
else:
    inner_a = args.horizontal_radius - 1.
    inner_b = args.vertical_radius - 1.
    outer_a = args.horizontal_radius
    outer_b = args.vertical_radius
    inner_ellipse = Ellipse(inner_a, inner_b, angle)
    outer_ellipse = Ellipse(outer_a, outer_b, angle)
    min_x = -30
    max_x = 30
    min_y = -30
    max_y = 30

    inner_set = set()
    for x in range(min_x, max_x + 1, 1):
        y_pair = inner_ellipse.solve_y(x)
        if y_pair:
            inner_set.add((x, y_pair[0]))
            inner_set.add((x, y_pair[1]))

    for y in range(min_y, max_y + 1, 1):
        x_pair = inner_ellipse.solve_x(y)
        if x_pair:
            inner_set.add((x_pair[0], y))
            inner_set.add((x_pair[1], y))

    outer_set = set()
    for x in range(min_x, max_x + 1, 1):
        y_pair = outer_ellipse.solve_y(x)
        if y_pair:
            outer_set.add((x, y_pair[0]))
            outer_set.add((x, y_pair[1]))

    for y in range(min_y, max_y + 1, 1):
        x_pair = outer_ellipse.solve_x(y)
        if x_pair:
            outer_set.add((x_pair[0], y))
            outer_set.add((x_pair[1], y))

    print("Inner coordinates:")
    for i in inner_set:
        print("{}\t{}".format(i[0], i[1]))

    print("\nOuter coordinates:")
    for i in outer_set:
        print("{}\t{}".format(i[0], i[1]))
