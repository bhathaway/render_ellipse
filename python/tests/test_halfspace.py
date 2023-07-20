from ascii_shapes import convex_polygon
import unittest

class TestHalfSpace(unittest.TestCase):
    def test_basics(self):
        h = convex_polygon.HalfSpace((0, 0), (1, 0))
        self.assertTrue(h.contains((0, 0)))
        self.assertTrue(h.contains((0, 1)))
        self.assertFalse(h.contains((0, -1)))

        x = h.intersection((0, -1), (1, 1))
        self.assertEqual(x, (0.5, 0.0))

if __name__ == '__main__':
    unittest.main()

