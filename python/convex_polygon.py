
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

    def __repr__(self):
        return "<{}, {}>".format(self.x, self.y)

# As always, counterclockwise.
class HalfSpace:
    def __init__(self, start, end):
        assert(type(start) == tuple)
        assert(len(start) >= 2)
        assert(type(end) == tuple)
        assert(len(end) >= 2)
        self.point = start
        v = Vector2d(end[0] - start[0], end[1] - start[1])
        self.alt_point = end
        self.normal = v.normal()

    def contains(self, p):
        assert(type(p) == tuple)
        assert(len(p) >= 2)
        test = Vector2d(p[0] - self.point[0],
          p[1] - self.point[1])
        return self.normal.dot(test) >= 0

    def intersection(self, start, end):
        assert(type(start) == tuple)
        assert(len(start) >= 2)
        assert(type(end) == tuple)
        assert(len(end) >= 2)
        v0 = Vector2d(start[0] - self.point[0],
          start[1] - self.point[1])
        v1 = Vector2d(end[0] - self.point[0],
          end[1] - self.point[1])
        q = v0.dot(self.normal)
        r = v1.dot(self.normal)
        if q-r == 0:
            return None
        t = 1.*q / (q-r)
        v = Vector2d(end[0] - start[0], end[1] - start[1])
        return (start[0] + t*v.x, start[1] + t*v.y)

# I got the area equation from here:
# https://www.mathwords.com/a/area_convex_polygon.htm

# Important is this assumes a counterclockwise convention for positive
# area. If you reverse the ordering, the areas will be negative.
class ConvexPolygon:
    def __init__(self, vertices):
        assert(type(vertices) == list)
        assert(all(map(lambda x: type(x) == tuple, vertices)))
        assert(all(map(lambda x: len(x) >= 2, vertices)))
        self.vertices = vertices

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
            pos_diag_sum += v[i][0] * v[k][1]
            neg_diag_sum += v[i][1] * v[k][0]
        return (pos_diag_sum - neg_diag_sum) / 2.0

    def trim(self, start, end):
        assert(type(start) == tuple)
        assert(len(start) >= 2)
        assert(type(end) == tuple)
        assert(len(end) >= 2)
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

