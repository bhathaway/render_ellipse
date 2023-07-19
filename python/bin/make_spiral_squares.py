#! /usr/bin/env python

import sys
sys.path.append('..')
import math
from pixel_square import *

import argparse as ap
parser = ap.ArgumentParser(description='Make ASCII art square spiral')
parser.add_argument('-S', '--start_length', type=float, required=True,
    help='starting length of square side')
parser.add_argument('-E', '--ending_length', type=float, required=True,
    help='ending length of square side')
parser.add_argument('-A', '--starting_angle', type=float, default = 0.0,
    help='Starting angle in degrees')
parser.add_argument('-T', '--total_angle', type=float, default = 90.0,
    help='Swept angle in degrees')
parser.add_argument('-H', '--height', type=int, default = 10,
    help='Height of extrusion')
parser.add_argument('-x', '--nudgex', type=float, default = 0.0,
    help='x translation applied after rotation (-1, 1)')
parser.add_argument('-y', '--nudgey', type=float, default = 0.0,
    help='y translation applied after rotation (-1, 1)')

args = parser.parse_args()
start_angle = (args.starting_angle + 45.0) * math.pi / 180.0
d_th = (args.total_angle / (args.height - 1)) * math.pi / 180.0

d_x = (args.ending_length - args.start_length) / (args.height - 1)

for level in range(args.height):
    print("level: {}".format(level + 1))
    angle = start_angle + d_th * level
    side = args.start_length + d_x * level
    print(raster_square(side, angle, (args.nudgex, args.nudgey)))

