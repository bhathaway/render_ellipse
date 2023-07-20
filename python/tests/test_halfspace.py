from ascii_shapes.convex_polygon import (
    HalfSpace,
    Point2d as P
    )
import unittest

class TestHalfSpace(unittest.TestCase):
    def test_basics(self):
        h = HalfSpace(P(0, 0), P(1, 0))
        self.assertTrue(h.contains(P(0, 0)))
        self.assertTrue(h.contains(P(0, 1)))
        self.assertFalse(h.contains(P(0, -1)))

        x = h.intersection(P(0, -1), P(1, 1))
        self.assertEqual(x, P(0.5, 0.0))

if __name__ == '__main__':
    unittest.main()

