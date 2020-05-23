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
