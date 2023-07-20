from ascii_shapes.convex_polygon import Vector2d
import unittest

class TestVector2d(unittest.TestCase):
    def test_basics(self):
        v = Vector2d(1, 2)
        n1 = v.normal()
        self.assertEqual(n1.x, -2)
        self.assertEqual(n1.y, 1)
        self.assertEqual(v.dot(n1), 0)

if __name__ == '__main__':
    unittest.main()

