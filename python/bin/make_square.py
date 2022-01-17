#! /usr/bin/env python

import sys
sys.path.append('..')
import math
from pixel_square import *

import argparse as ap
parser = ap.ArgumentParser(description='Make ASCII art square')
parser.add_argument('-S', '--side_length', type=float, required=True,
    help='length of square side')
parser.add_argument('-A', '--angle', type=float, default = 0.0,
    help='Angle to rotate clockwise in degrees')
parser.add_argument('-x', '--nudgex', type=float, default = 0.0,
    help='x translation applied after rotation (-1, 1)')
parser.add_argument('-y', '--nudgey', type=float, default = 0.0,
    help='y translation applied after rotation (-1, 1)')

args = parser.parse_args()
angle = (args.angle + 45.0) * math.pi / 180.0

print(raster_square(args.side_length, angle, (args.nudgex, args.nudgey)))

