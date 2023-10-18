#pragma once
#include "convex_polygon.h"

#include "spdlog/spdlog.h"

#include <set>
#include <map>

// The concept here is that this pixel is part of a larger traced shape of
// some thickness where the interior of that shape is conventionally at (0, 0)
// By trimming these pixels, we can decide how to render them based on their
// area. Method `trim_outer` is for trimming from the exterior of the traced shape,
// and `trim_inner` is for trimming from the interior.
class Pixel {
public:
  Pixel(double x, double y);

  Pixel(const Pixel&) = default;
  Pixel& operator=(const Pixel&) = default;

  void trim_outer(const Point2d& p0, const Point2d& p1, bool reversed = false);
  void trim_inner(const Point2d& p0, const Point2d& p1);

  // Use to get vertices or area
  const ConvexPolygon& poly() const;

  const double x() const { return corner_.x(); }
  const double y() const { return corner_.y(); }

  bool operator<(const Pixel& p) const { return corner_ < p.corner_; }

private:
  Point2d corner_;
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

  static std::shared_ptr<spdlog::logger> logger;
};

struct RasterResult {
  double x_min;
  double y_min;
  double x_max;
  double y_max;
  std::map<Point2d, Pixel> points_to_pixels;
};

// The arguments here are for the outer edge of the ellipse.
// The inner ellipse is implicity 1 pixel thick.
RasterResult raster_ellipse(double a, double b, double th, const Vector2d& nudge);

// Returns an ascii art representation of the rasterization.
// In the future it should be possible to create other kinds of images.
std::string ascii_render(const RasterResult&);

