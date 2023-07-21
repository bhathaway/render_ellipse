#pragma once
#include "convex_polygon.h"
#include <set>

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

  const double x() const { return x_; }
  const double y() const { return y_; }

private:
  double x_;
  double y_;
  ConvexPolygon poly_;
};

class Ellipse {
public:
  // a: radius along x direction
  // b: radius along y direction
  // th: angular displacement from x-axis in radians.
  // nudge: nudges the ellipse to help get best looking pixels
  Ellipse(double a, double b, double th, const Vector2d& nudge);

  // Needed for the solution below
  double y_determinant(double x) const;

  // Returns a pair of y intercepts for an x value. `det` is non-negative
  std::pair<double, double> solve_y(double x, double det) const;

  // Needed for the solution below
  double x_determinant(double y) const;

  // Returns a pair of x intercepts for a y value. `det` is non-negative
  std::pair<double, double> solve_x(double y, double det) const;

  std::vector<Point2d> points_on_grid() const;
  std::set<Point2d> points_in_pixel(const Pixel&) const;

private:
  // These are parts of the ellipse equation that won't change, so
  // we can set them up as constants.
  double memo_a_;
  double memo_b_;
  double memo_c_;
  Vector2d nudge_; // Moved from origin to facilitate aliases.
};
