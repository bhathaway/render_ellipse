#include "pixel_ellipse.h"
#include <cmath>

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

Ellipse::Ellipse(double a, double b, double th, const Vector2d& nudge)
: nudge_(nudge)
{
  const double c = cos(th);
  const double s = sin(th);

  memo_a_ = (c*c)/(a*a) + (s*s)/(b*b);
  memo_b_ = 2*c*s*(1.0/(a*a) - 1.0/(b*b));
  memo_c_ = (s*s)/(a*a) + (c*c)/(b*b);
}

double Ellipse::y_determinant(double x) const
{
  const double& A = memo_a_;
  const double& B = memo_b_;
  const double& C = memo_c_;

  const double u = x - nudge_.x();
  return -4*A*C*u*u + B*B*u*u + 4*C;
}

std::pair<double, double> Ellipse::solve_y(double x, double det) const
{
  assert(det >= 0);
  const double& B = memo_b_;
  const double& C = memo_c_;

  const double r = sqrt(det);
  const double u = x - nudge_.x();

  return std::pair<double, double> {
     (r-B*u) / (2*C) + nudge_.y(),
    (-r-B*u) / (2*C) + nudge_.y()
  };
}

double Ellipse::x_determinant(double y) const
{
  const double& A = memo_a_;
  const double& B = memo_b_;
  const double& C = memo_c_;

  const double v = y - nudge_.y();
  return -4*A*C*v*v + B*B*v*v + 4*A;
}

std::pair<double, double> Ellipse::solve_x(double y, double det) const
{
  assert(det >= 0);
  const double& A = memo_a_;
  const double& B = memo_b_;

  const double r = sqrt(det);
  const double v = y - nudge_.y();

  return std::pair<double, double> {
     (r-B*v) / (2*A) + nudge_.x(),
    (-r-B*v) / (2*A) + nudge_.x()
  };
}

std::vector<Point2d> Ellipse::points_on_grid() const
{
  std::vector<Point2d> points;

  auto get_x_intercepts = [&](double x) -> bool {
    const double det = y_determinant(x);
    if (det >= 0) {
      auto pair = solve_y(x, det);
      points.emplace_back(x, pair.first);
      points.emplace_back(x, pair.second);
      return true;
    } else {
      return false;
    }
  };

  auto get_y_intercepts = [&](double y) -> bool {
    const double det = x_determinant(y);
    if (det >= 0) {
      auto pair = solve_x(y, det);
      points.emplace_back(pair.first, y);
      points.emplace_back(pair.second, y);
      return true;
    } else {
      return false;
    }
  };

  for (double x = 0; get_x_intercepts(x); x += 1)
  { }

  for (double x = -1; get_x_intercepts(x); x -= 1)
  { }

  for (double y = 0; get_y_intercepts(y); y += 1)
  { }

  for (double y = -1; get_y_intercepts(y); y -= 1)
  { }

  return points;
}

std::set<Point2d> Ellipse::points_in_pixel(const Pixel& p) const
{
  const double x = p.x();
  const double y = p.y();
  const double eps = 0.00001;

  std::set<Point2d> points;

  // Lower edge
  double det = x_determinant(y);
  if (det >= 0) {
    auto pair = solve_x(y, det);
    const double x0 = pair.first;
    const double x1 = pair.second;
    if (std::abs(x0 - x1) > eps) {
      if (x0 >= x && x0 <= x + 1)
        points.emplace(Point2d(x0, y));
      if (x1 >= x && x1 <= x + 1)
        points.emplace(Point2d(x1, y));
    }
  }

  // Right edge
  det = y_determinant(x + 1);
  if (det >= 0) {
    auto pair = solve_y(x, det);
    const double y0 = pair.first;
    const double y1 = pair.second;
    if (std::abs(y0 - y1) > eps) {
      if (y0 >= y && y0 <= y + 1)
        points.emplace(Point2d(x + 1, y0));
      if (y1 >= y && y1 <= y + 1)
        points.emplace(Point2d(x + 1, y1));
    }
  }

  // Upper edge
  det = x_determinant(y + 1);
  if (det >= 0) {
    auto pair = solve_x(y, det);
    const double x0 = pair.first;
    const double x1 = pair.second;
    if (std::abs(x0 - x1) > eps) {
      if (x0 >= x && x0 <= x + 1)
        points.emplace(Point2d(x0, y + 1));
      if (x1 >= x && x1 <= x + 1)
        points.emplace(Point2d(x1, y + 1));
    }
  }

  // Left edge
  det = y_determinant(x);
  if (det >= 0) {
    auto pair = solve_y(x, det);
    const double y0 = pair.first;
    const double y1 = pair.second;
    if (std::abs(y0 - y1) > eps) {
      if (y0 >= y && y0 <= y + 1)
        points.emplace(Point2d(x, y0));
      if (y1 >= y && y1 <= y + 1)
        points.emplace(Point2d(x, y1));
    }
  }

  return points;
}
