from ascii_shapes import pixel_ellipse
import unittest

class TestTrimPixels(unittest.TestCase):
    def test_trim_cw(self):
        # Convensionally, pixel defined by lower left.
        p = pixel_ellipse.Pixel(0.0, 0.0)
        p.trim_outer((1.0, 0.5), (0.5, 1.0))
        p.trim_inner((0.0, 0.5), (0.5, 0.0))
        self.assertEqual(p.poly.area(), 0.75)

    def test_trim_ccw(self):
        q = pixel_ellipse.Pixel(0.0, 0.0)
        q.trim_outer((0.5, 1.0), (1.0, 0.5))
        q.trim_inner((0.5, 0.0), (0.0, 0.5))
        self.assertEqual(q.poly.area(), 0.75)

if __name__ == '__main__':
    unittest.main()

