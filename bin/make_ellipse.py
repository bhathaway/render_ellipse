#! /usr/bin/env python

import sys
sys.path.append('..')
import math
from pixel_ellipse import *

import argparse as ap
parser = ap.ArgumentParser(description='Make ASCII art ellipse')
parser.add_argument('-X', '--horizontal_radius', type=float, required=True,
    help='distance from center to horizontal edge')
parser.add_argument('-Y', '--vertical_radius', type=float, required=True,
    help='distance from center to vertical edge')
parser.add_argument('-A', '--angle', type=float, default=0.0,
    help='Angle to rotate clockwise in degrees')

args = parser.parse_args()

angle = args.angle * math.pi / 180.0
r = raster_ellipse(args.horizontal_radius, args.vertical_radius, angle)

print(render_raster(r))

