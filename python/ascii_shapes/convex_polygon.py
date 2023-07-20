
class Vector2d(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y

    # Counter clockwise normal
    def normal(self):
        return Vector2d(-self.y, self.x)

    def dot(self, v):
        assert(type(v) == Vector2d)
        return self.x * v.x + self.y * v.y

    def scaled_by(self, s):
        return Vector2d(s * self.x, s * self.y)

    def __eq__(self, v):
        return self.x == v.x and self.y == v.y

    def __repr__(self):
        return "v<{}, {}>".format(self.x, self.y)

class Point2d(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def minus(self, p):
        assert(type(p) == Point2d)
        return Vector2d(self.x - p.x, self.y - p.y)

    def plus(self, v):
        assert(type(v) == Vector2d)
        return Point2d(self.x + v.x, self.y + v.y)

    def __eq__(self, p):
        return self.x == p.x and self.y == p.y

    # Needed for set operations
    def __hash__(self):
        return hash((self.x, self.y))

    def __repr__(self):
        return "p({}, {})".format(self.x, self.y)

# As always, counterclockwise.
class HalfSpace:
    def __init__(self, start, end):
        assert(type(start) == Point2d)
        assert(type(end) == Point2d)
        self.point = start
        v = end.minus(start)
        self.normal = v.normal()

    def contains(self, p):
        assert(type(p) == Point2d)
        test = p.minus(self.point)
        return self.normal.dot(test) >= 0

    def intersection(self, start, end):
        assert(type(start) == Point2d)
        assert(type(end) == Point2d)
        v0 = start.minus(self.point)
        v1 = end.minus(self.point)
        q = v0.dot(self.normal)
        r = v1.dot(self.normal)
        if q-r == 0:
            return None
        t = 1.*q / (q-r)
        v = end.minus(start)
        return start.plus(v.scaled_by(t))

# I got the area equation from here:
# https://www.mathwords.com/a/area_convex_polygon.htm

# Important is this assumes a counterclockwise convention for positive
# area. If you reverse the ordering, the areas will be negative.
class ConvexPolygon:
    def __init__(self, vertices):
        assert(type(vertices) == list)
        assert(all(map(lambda x: type(x) == Point2d, vertices)))
        self.vertices = vertices
        self.half_spaces = []
        for i in range(len(self.vertices)):
            next_i = i + 1
            if next_i == len(self.vertices):
                next_i = 0
            self.half_spaces.append(\
              HalfSpace(self.vertices[i], self.vertices[next_i]))

    def edge_count(self):
        return len(self.vertices)

    def get_vertex(self, i):
        return self.vertices[i]

    def area(self):
        pos_diag_sum = 0.0
        neg_diag_sum = 0.0
        m = len(self.vertices)
        v = self.vertices
        for i in range(m):
            k = i + 1
            if k >= m:
                k = 0
            pos_diag_sum += v[i].x * v[k].y
            neg_diag_sum += v[i].y * v[k].x
        return (pos_diag_sum - neg_diag_sum) / 2.0

    def trim(self, start, end):
        h = HalfSpace(start, end)
        in_v = self.vertices
        out_v = []
        for i in range(len(in_v)):
            cur_point = in_v[i]
            if i == 0:
                prev_point = in_v[-1]
            else:
                prev_point = in_v[i-1]
            if h.contains(cur_point):
                if not h.contains(prev_point):
                    out_v.append(h.intersection(prev_point, cur_point))
                out_v.append(cur_point)
            elif h.contains(prev_point):
                out_v.append(h.intersection(prev_point, cur_point))
        self.vertices = out_v
    
    def contains(self, p):
        for h in self.half_spaces:
            if not h.contains(p):
                return False
        return True

