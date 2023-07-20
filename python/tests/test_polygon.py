from ascii_shapes.convex_polygon import ConvexPolygon
from math import *
import unittest

class TestConvexPolygon(unittest.TestCase):
    def test_neg_area(self):
        l = [(-4, 3), (2, 5), (5, 1)]
        c = ConvexPolygon(l)
        # Expect negative area for cw orientation.
        self.assertEqual(c.area(), -15)

    def test_getters_plus_basics(self):
        l = [(-4, 3), (5, 1), (2, 5)]
        c = ConvexPolygon(l)
        self.assertEqual(c.edge_count(), 3)
        self.assertEqual(c.get_vertex(0), (-4, 3))
        self.assertEqual(c.get_vertex(1), (5, 1))
        self.assertEqual(c.get_vertex(2), (2, 5))
        self.assertEqual(c.area(), 15)

    def test_ccw_pixel(self):
        l = [(0, 0), (1, 0), (1, 1), (0, 1)]
        s = ConvexPolygon(l)
        self.assertEqual(s.area(), 1)

    def test_hexagon(self):
        s_3 = sqrt(3.0)
        l = [(0, 0), (1, 0), (1.5, s_3/2.0), (1, s_3), (0, s_3), (-0.5, s_3/2.0)]
        h = ConvexPolygon(l)
        self.assertAlmostEqual(h.area(), 1.5 * s_3)

if __name__ == '__main__':
    unittest.main()

