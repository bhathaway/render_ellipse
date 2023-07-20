#pragma once
#include "convex_polygon.h"

// The concept here is that this pixel is part of a larger traced shape of
// some thickness where the interior of that shape is conventionally at (0, 0)
// By trimming these pixels, we can decide how to render them based on their
// area. Method `trim_outer` is for trimming from the exterior of the traced shape,
// and `trim_inner` is for trimming from the interior.
class Pixel {
public:
  Pixel(double x, double y);

  void trim_outer(Point2d& p0, Point2d& p1, bool reversed = false);
  void trim_inner(Point2d& p0, Point2d& p1);

  // Use to get vertices or area
  const ConvexPolygon& poly() const;

private:
  double x_;
  double y_;
  ConvexPolygon poly_;
};

class Ellipse {
public:
  Ellipse(double a, double b, double th, double nudge_x = 0, double nudge_y = 0);

private:

};
