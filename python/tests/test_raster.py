from ascii_shapes.pixel_ellipse import *
from ascii_shapes.convex_polygon import Vector2d as V
import unittest

class TestRaster(unittest.TestCase):
    def test_basic_circle(self):
        self.maxDiff = None
        expected_output = str(
            '            \n'
            '   .oOOo.   \n'
            '  oO.  .Oo  \n'
            ' .O      O. \n'
            ' o.      .o \n'
            ' O        O \n'
            ' O        O \n'
            ' o.      .o \n'
            ' .O      O. \n'
            '  oO.  .Oo  \n'
            '   .oOOo.   \n'
            '            \n'
        )

        p = raster_ellipse(5, 5, 0.0, V(0.0, 0.0))

        s = ascii_render(p)
        self.assertEqual(s, expected_output)

    def test_raster_then_render(self):
        self.maxDiff = None
        expected_output = str(
            '                    .ooOOOOo.         \n'
            '                 .OOo..    .oOO.      \n'
            '               oOo             oO     \n'
            '             oO.                .O    \n'
            '           .Oo                   .O   \n'
            '          oO                      oo  \n'
            '         Oo                        O  \n'
            '        O.                         oo \n'
            '       O.                           O \n'
            '      O.                            O \n'
            '     oo                             O \n'
            '    .O                              O \n'
            '    O                               O \n'
            '   o.                               O \n'
            '   O                               .o \n'
            '  o.                               o. \n'
            '  O                                O  \n'
            ' .o                               .o  \n'
            ' o.                               O   \n'
            ' O                               .o   \n'
            ' O                               O    \n'
            ' O                              O.    \n'
            ' O                             oo     \n'
            ' O                            .O      \n'
            ' O                           .O       \n'
            ' oo                         .O        \n'
            '  O                        oO         \n'
            '  oo                      Oo          \n'
            '   O.                   oO.           \n'
            '    O.                .Oo             \n'
            '     Oo             oOo               \n'
            '      .OOo.    ..oOO.                 \n'
            '         .oOOOOoo.                    \n'
        )

        p = raster_ellipse(20, 14, 0.64, V(0.0, 0.5))

        s = ascii_render(p)
        self.assertEqual(s, expected_output)

if __name__ == '__main__':
    unittest.main()

