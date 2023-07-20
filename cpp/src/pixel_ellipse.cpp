#include "pixel_ellipse.h"

Pixel::Pixel(double x, double y)
: x_(x), y_(y)
{
  std::vector<Point2d> points;
  points.emplace_back(x, y);
  points.emplace_back(x + 1, y);
  points.emplace_back(x + 1, y + 1);
  points.emplace_back(x, y + 1);
  poly_ = ConvexPolygon(points);
}

void Pixel::trim_outer(Point2d& p0, Point2d& p1, bool reversed)
{
  std::vector<Point2d> points;
  points.emplace_back(0, 0);
  points.push_back(p0);
  points.push_back(p1);
  ConvexPolygon wedge(points);
  double eps = 0.00001;
  double area = wedge.area();

  double swap = false;
  if (std::abs(area) < eps) {
    return;
  } else if (reversed) {
    if (area > 0)
      swap = true;
  } else {
    if (area < 0)
      swap = true;
  }

  if (swap)
    std::swap(p0, p1);

  poly_.trim(p0, p1);
}

void Pixel::trim_inner(Point2d& p0, Point2d& p1)
{
  constexpr bool reversed = true;
  trim_outer(p0, p1, reversed);
}

const ConvexPolygon& Pixel::poly() const
{
  return poly_;
}
