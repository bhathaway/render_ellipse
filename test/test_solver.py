from pixel_ellipse import *

outer_a = 20
outer_b = 14
theta = 0.64
inner_a = 16
inner_b = 10

min_x = -20
max_x = 20
min_y = -20
max_y = 20

inner_ellipse = Ellipse(inner_a, inner_b, theta)
outer_ellipse = Ellipse(outer_a, outer_b, theta)

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

